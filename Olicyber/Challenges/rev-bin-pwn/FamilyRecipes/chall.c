#include <linux/fs.h> 
#include <linux/cred.h>
#include <linux/uaccess.h>
#include <linux/spinlock.h>
#include <linux/miscdevice.h>

#define CMD_ALLOC 1337
#define CMD_DELETE 1338
#define CMD_READ 1339
#define CMD_INFO 1340
#define CMD_TOGGLE 1341
#define MAX_BUFSIZE 1024

static DEFINE_SPINLOCK(lock);

typedef union request {

	struct alloc {
		unsigned long idx;
		char* buf;
		unsigned long bufsize;
		unsigned int public;
	} alloc;

	struct delete {
		unsigned long idx;
	} delete;

	struct read {
		unsigned long idx;
		char *buf;
		unsigned long bufsize;
	} read;

	struct info {
		unsigned long idx;
		unsigned long bufsize;
		unsigned int public;
		uid_t owner_uid;
	} info;

	struct toggle {
		unsigned long idx;
	} toggle;

} request_t;

typedef struct recipe {
	char *buf;
	unsigned long bufsize;
	unsigned int public;
	uid_t owner_uid;
} recipe_t;

typedef struct recipe_manager {
	recipe_t **recipes_list;
	unsigned char num_of_recipes;
} recipe_manager_t;

recipe_manager_t manager;

static long dev_ioctl(struct file * file, unsigned int cmd, unsigned long arg) {

	request_t request;
	recipe_t *recipe;
	void *tmp;
	char *buf;
	unsigned long idx;

	spin_lock(&lock);

	if (copy_from_user(&request, (const request_t*)arg, sizeof(request))) {
		printk(KERN_INFO "[CHALL] [ERR] Request copy failed\n");
		goto error;
	}
		
	switch (cmd) {
		case CMD_ALLOC: {

			if (request.alloc.bufsize > MAX_BUFSIZE) {
				printk(KERN_INFO "[CHALL] [ERR] Recipe size too big\n");
				goto error;
			}

			for (unsigned long i = 0; i < manager.num_of_recipes; i++) {
				recipe = manager.recipes_list[i];
				if (ZERO_OR_NULL_PTR(recipe)) {
					idx = i;
					goto allocate_recipe;
				}
			}

			idx = manager.num_of_recipes;
			manager.num_of_recipes++;
			
			if (manager.recipes_list == NULL) {
				tmp = kmalloc(sizeof(recipe_t *) * manager.num_of_recipes, GFP_KERNEL);
			} else {
				tmp = krealloc(manager.recipes_list, sizeof(recipe_t *) * manager.num_of_recipes, GFP_KERNEL);
			}

			if (ZERO_OR_NULL_PTR(tmp)) {
				printk(KERN_INFO "[CHALL] [ERR] (Re)allocation failed\n");
				manager.num_of_recipes--;
				goto error;
			}

			manager.recipes_list = tmp;

allocate_recipe:
			recipe = kmalloc(sizeof(recipe_t), GFP_KERNEL);

			if (ZERO_OR_NULL_PTR(recipe)) {
				printk(KERN_INFO "[CHALL] [ERR] New recipe allocation failed\n");
				manager.recipes_list[idx] = NULL;
				goto error;
			}

			buf = kmalloc(sizeof(char) * request.alloc.bufsize + 1, GFP_KERNEL);

			if (ZERO_OR_NULL_PTR(buf)) {
				printk(KERN_INFO "[CHALL] [ERR] Recipe buffer allocation failed\n");
				if (!ZERO_OR_NULL_PTR(recipe)) {
					kfree(recipe);
				}
				manager.recipes_list[idx] = NULL;
				goto error;
			}

			recipe->buf = buf;
			recipe->bufsize = request.alloc.bufsize;
			recipe->public = request.alloc.public ? 1 : 0;
			recipe->owner_uid = current_uid().val;

			if (copy_from_user(recipe->buf, request.alloc.buf, request.alloc.bufsize)) {
				printk(KERN_INFO "[CHALL] [ERR] Buffer data copy failed\n");
				if (!ZERO_OR_NULL_PTR(recipe)) {
					kfree(recipe->buf);
				}
				if (!ZERO_OR_NULL_PTR(recipe)) {
					kfree(recipe);
				}
				manager.recipes_list[idx] = NULL;
				goto error;
			}
			
			recipe->buf[recipe->bufsize] = '\0';

			manager.recipes_list[idx] = recipe;

			request.alloc.idx = idx;

			if (copy_to_user((request_t*)arg, (const request_t*)&request, sizeof(request))) {
				printk(KERN_INFO "[CHALL] [ERR] Copy to user failed\n");
				goto error;
			}
			
			goto success;
		}
		case CMD_DELETE:
		case CMD_READ:
		case CMD_INFO: 
		case CMD_TOGGLE: {

			if (cmd == CMD_DELETE) {
				idx = request.delete.idx;
			} else if (cmd == CMD_READ) {
				idx = request.read.idx;
			} else if (cmd == CMD_INFO) {
				idx = request.info.idx;
			} else if (cmd == CMD_TOGGLE) {
				idx = request.toggle.idx;
			}

			if (idx >= manager.num_of_recipes) {
				printk(KERN_INFO "[CHALL] [ERR] Index out of range\n");
				goto error;
			}

			recipe = manager.recipes_list[idx];
			if (ZERO_OR_NULL_PTR(recipe)) {
				printk(KERN_INFO "[CHALL] [ERR] Recipe deleted\n");
				goto error;
			}

			if (cmd == CMD_DELETE || cmd == CMD_TOGGLE || (cmd == CMD_READ && !recipe->public)) {
				if (recipe->owner_uid != current_uid().val) {
					printk(KERN_INFO "[CHALL] [ERR] User is not recipe owner\n");
					goto error;
				}				
			}

			if (cmd == CMD_DELETE) {

				if (!ZERO_OR_NULL_PTR(recipe->buf)) {
					kfree(recipe->buf);
				}
				kfree(recipe);
				manager.recipes_list[request.delete.idx] = NULL;

			} else if (cmd == CMD_READ) {

				if (request.read.bufsize > recipe->bufsize) {
					printk(KERN_INFO "[CHALL] [ERR] Requested bufsize > real bufsize\n");
					goto error;
				}

				if (copy_to_user(request.read.buf, recipe->buf, request.read.bufsize)) {
					printk(KERN_INFO "[CHALL] [ERR] Copy to user failed\n");
					goto error;
				}

			} else if (cmd == CMD_INFO) {
				
				request.info.bufsize = recipe->bufsize;
				request.info.owner_uid = recipe->owner_uid;
				request.info.public = recipe->public;

				if (copy_to_user(( request_t*)arg, (const request_t*)&request, sizeof(request))) {
					printk(KERN_INFO "[CHALL] [ERR] Copy to user failed\n");
					goto error;
				}

			} else if (cmd == CMD_TOGGLE) {
				
				recipe->public = recipe->public ? 0 : 1;

			}
			
			goto success;

		}
	}

error:
	spin_unlock(&lock);
	return -1;

success:
	spin_unlock(&lock);
	return 0;

}

static int dev_open(struct inode *inode, struct file *file) {
	
	file->private_data = NULL;
	return 0;
}

static int dev_release(struct inode *inode, struct file *file) {
	return 0;
}

static struct file_operations chall_fops = {
	.open = dev_open,
	.release = dev_release,
    .unlocked_ioctl = dev_ioctl
};

struct miscdevice chall_dev = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = "chall",
    .fops = &chall_fops,
};

static int __init init_dev(void) {

    if (misc_register(&chall_dev) < 0) {
        printk(KERN_INFO "[CHALL] [ERR] Failed to register device\n");
		return -1;
	}

	manager.recipes_list = NULL;
	manager.num_of_recipes = 0;

	return 0;
}

static void __exit exit_dev(void) {
	
	recipe_t *recipe;

	for (unsigned long i = 0; i < manager.num_of_recipes; i++) {

		recipe = manager.recipes_list[i];
		
		if (ZERO_OR_NULL_PTR(recipe)) {
			continue;
		}
		
		if (!ZERO_OR_NULL_PTR(recipe->buf)) {
			kfree(recipe->buf);
		}
		kfree(recipe);

		manager.recipes_list[i] = NULL;

	}
	
	if (!ZERO_OR_NULL_PTR(manager.recipes_list)) {
		kfree(manager.recipes_list);
	}

	misc_deregister(&chall_dev);

}

module_init(init_dev);
module_exit(exit_dev);

MODULE_AUTHOR("@giulia");                    
MODULE_DESCRIPTION("Challenge");
MODULE_LICENSE("GPL");
