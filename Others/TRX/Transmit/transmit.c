#include <asm/uaccess.h>
#include <linux/atmdev.h>
#include <linux/cdev.h>
#include <linux/errno.h>
#include <linux/fs.h>
#include <linux/futex.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/sched.h>
#include <net/tcp.h>

#define DEVICE_NAME "transmit"

#define CREATE_SESSION 0
#define DESTROY_SESSION 1
#define TEST_SESSION 2 // TODO: Implement TEST_SESSION
#define TRANSMIT_FAST 3
#define TRANSMIT_NORMAL 4
#define COPY_DATA 5
#define READ_DATA 6
#define DELETE_DATA 7

#define LOG_PREFIX "[" DEVICE_NAME "] "
#define LOG_ERROR(fmt, ...) printk(KERN_ERR LOG_PREFIX fmt "\n", ##__VA_ARGS__)
#define LOG_NOTICE(fmt, ...)                                                   \
  printk(KERN_NOTICE LOG_PREFIX fmt "\n", ##__VA_ARGS__)
#define LOG_DEBUG(fmt, ...)                                                    \
  printk(KERN_DEBUG LOG_PREFIX fmt "\n", ##__VA_ARGS__)
#define MAX_SESSIONS 255

struct session {
  u32 id;
  void *data;
  u64 data_len;
  bool is_fast;
};

struct device_arg {
  u32 id;
  void *data;
  u64 data_len;
  u32 to_id;
  u32 from_id;
};

static struct session *sessions[MAX_SESSIONS];
static bool fast_session_active = false;
static int session_idx = 0;
static struct class *class;
static int major_no;

static struct session *find_session_by_id(u32 id) {
  for (int i = 0; i < MAX_SESSIONS; i++) {
    if (sessions[i] && sessions[i]->id == id) {
      return sessions[i];
    }
  }
  return NULL;
}

static int copy_arg_from_user(struct device_arg *arg_ptr,
                              unsigned long user_arg) {

  if (user_arg != 0 &&
      copy_from_user(arg_ptr, (struct device_arg __user *)user_arg,
                     sizeof(struct device_arg))) {
    LOG_ERROR("Failed to copy data from user space.");
    return -EFAULT;
  }
  return 0;
}

static long handle_ioctl(struct file *file, unsigned int cmd, unsigned long arg,
                         bool is_compat) {
  struct device_arg device_arg;
  struct session *session = NULL;
  int ret_val;
  ret_val = copy_arg_from_user(&device_arg, arg);
  if (ret_val != 0) {
    return ret_val;
  }
  switch (cmd) {
  case CREATE_SESSION:
    LOG_NOTICE("TCP SESSION CREATED");
    session = (struct session *)kzalloc(sizeof(struct session), GFP_ATOMIC);
    if (!session) {
      LOG_ERROR("Failed to allocate memory for session.");
      return -ENOMEM;
    }

    if (is_compat) {
      session->id = hash32_ptr(&tcp_hashinfo + session_idx);
    } else {
      session->id = hash_ptr(&tcp_hashinfo + session_idx, 64);
    }
    sessions[session_idx] = session;
    session_idx++;
    return session->id;
  case DESTROY_SESSION:
    LOG_NOTICE("TCP SESSION DESTROYED");
    if (session_idx < 0 || session_idx >= MAX_SESSIONS ||
        !sessions[session_idx]) {
      LOG_ERROR("Invalid session index.");
      return -EINVAL; // Invalid argument error
    }
    session = sessions[session_idx];
    if (session->data && !session->is_fast) {
      kfree(session->data);
      session->data = NULL;
    }
    kfree(session);
    sessions[session_idx] = NULL;
    session_idx--;
    return session_idx;
  case TRANSMIT_NORMAL:
    LOG_NOTICE("TCP TRANSMIT");
    session = find_session_by_id(device_arg.id);
    if (!session) {
      LOG_ERROR("Session not found.");
      return -ENOENT;
    }
    session->data = kmalloc(device_arg.data_len, GFP_KERNEL);
    if (!session->data) {
      LOG_ERROR("Failed to allocate memory for session data.");
      return -ENOMEM;
    }
    if (copy_from_user(session->data, device_arg.data, device_arg.data_len)) {
      LOG_ERROR("Failed to copy data from user space.");
      kfree(session->data);
      return -EFAULT;
    }
    session->data_len = device_arg.data_len;
    session->is_fast = false;
    return 0;
  case TRANSMIT_FAST:
    LOG_NOTICE("TCP TRANSMIT FAST");
    if (fast_session_active) {
      LOG_ERROR("Fast session already active.");
      return -EBUSY;
    }
    session = find_session_by_id(device_arg.id);
    if (!session) {
      LOG_ERROR("Session not found.");
      return -ENOENT;
    }
    session->data = (u64)device_arg.data;
    session->data_len = -1;
    session->is_fast = true;
    fast_session_active = true;
    return 0;
  case COPY_DATA:
    LOG_NOTICE("COPY DATA");
    struct session *from_session = NULL;
    struct session *to_session = NULL;

    if (device_arg.from_id == device_arg.to_id) {
      return 0;
    }

    from_session = find_session_by_id(device_arg.from_id);
    if (from_session == NULL) {
      LOG_ERROR("Source session not found.");
      return -ENOENT;
    }

    to_session = find_session_by_id(device_arg.to_id);

    if (to_session == NULL || from_session == NULL) {
      LOG_ERROR("Sssion not found.");
      return -ENOENT;
    } else if (from_session->is_fast && to_session->is_fast) {
      from_session->data = to_session->data;
    } else {
      if (to_session->data_len < from_session->data_len) {
        void *data = kmalloc(from_session->data_len, GFP_KERNEL);
        if (data == NULL) {
          LOG_ERROR("Failed to allocate memory for destination session data.");
          return -ENOMEM;
        }
        if (to_session->data) {
          kfree(to_session->data);
        }
        to_session->data = data;
      }
      memcpy(to_session->data, from_session->data, from_session->data_len);
    }
    return 0;
  case READ_DATA:
    // TODO: Implement READ_DATA
    break;
  case DELETE_DATA:
    // TODO: Implement DELETE_DATA
  default:
    LOG_ERROR("Invalid command: %u", cmd);
    return -EINVAL;
  }
  return 0;
}

static long device_file_unlocked_ioctl(struct file *file, unsigned int cmd,
                                       unsigned long arg) {
  return handle_ioctl(file, cmd, arg, false);
}

static long device_file_compat_ioctl(struct file *file, unsigned int cmd,
                                     unsigned long arg) {
  return handle_ioctl(file, cmd, arg, true);
};

static int device_file_open(struct inode *inode, struct file *file) {
  return 0;
}

static long device_file_read(struct file *file_ptr, char __user *user_buffer,
                             size_t count, loff_t *position) {
  return 0;
}

static long device_file_write(struct file *file_ptr,
                              const char __user *user_buffer, size_t count,
                              loff_t *position) {
  return -EINVAL; // Not implemented
}

static struct file_operations sample_driver_fops = {
    .owner = THIS_MODULE,
    .open = device_file_open,
    .read = device_file_read,
    .unlocked_ioctl = device_file_unlocked_ioctl,
    .compat_ioctl = device_file_compat_ioctl,
};

static int register_device(void) {
  major_no = register_chrdev(0, DEVICE_NAME, &sample_driver_fops);
  if (major_no < 0) {
    return major_no;
  }
  class = class_create(DEVICE_NAME);
  device_create(class, NULL, MKDEV(major_no, 0), NULL, DEVICE_NAME);
  return 0;
}

void unregister_device(void) {
  if (class != 0) {
    device_destroy(class, MKDEV(major_no, 0));
    class_unregister(class);

    unregister_chrdev(major_no, DEVICE_NAME);
  }
}

static int my_init(void) {
  register_device();
  return 0;
}

static void my_exit(void) {
  unregister_device();
  return;
}

module_init(my_init);
module_exit(my_exit);

MODULE_LICENSE("GPL");
