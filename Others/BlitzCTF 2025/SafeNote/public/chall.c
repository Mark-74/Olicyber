#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <fcntl.h>
#include <malloc.h>
#include <seccomp.h>
#include <limits.h>

#define MAX_NOTE 16
#define MAX_SIZE 0x2f8


static char *chunks[MAX_NOTE] = {0};
static uint16_t sizes[MAX_NOTE] = {0};


static void filter(void)
{
    scmp_filter_ctx ctx;

    ctx = seccomp_init(SCMP_ACT_KILL);
    if (!ctx)
    {
        puts("seccomp_init() error");
        exit(EXIT_FAILURE);
    }

    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 1,
                     SCMP_A0(SCMP_CMP_EQ, 0));
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 1,
                     SCMP_A0(SCMP_CMP_EQ, 1));
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(mprotect), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(close), 0);

    if (seccomp_load(ctx) < 0)
    {
        seccomp_release(ctx);
        puts("seccomp_load() error");
        exit(EXIT_FAILURE);
    }

    seccomp_release(ctx);
}


static void setup(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

static void menu()
{
    puts("");
    puts("Welcome to SafeNote!");
    puts("Please select an option:");
    puts("1. Create a note");
    puts("2. Read a note");
    puts("3. Edit a note");
    puts("4. Delete a note");
    puts("5. Exit");
    printf("Your choice: ");
}


static uint64_t get_uint()
{
    char buf[0x10];
    ssize_t bytes_read = read(0, buf, sizeof(buf) - 1);
    if (bytes_read <= 0)
    {
        return UINT64_MAX; // Read error or EOF
    }

    buf[bytes_read] = '\0';

    if (bytes_read > 0 && buf[bytes_read - 1] == '\n')
    {
        buf[bytes_read - 1] = '\0';
    }

    char *endptr;
    uint64_t num = strtoul(buf, &endptr, 10);

    if (endptr == buf || (*endptr != '\0' && *endptr != '\n' && *endptr != ' ' && *endptr != '\t'))
    {
        return UINT64_MAX; // Invalid input
    }

    return num;
}


static void create_note()
{

    uint64_t idx;
    uint64_t size;

    printf("Index of the note (0-%d): ", MAX_NOTE - 1);

    idx = get_uint();
    if (idx >= MAX_NOTE || idx == UINT64_MAX)
    {
        puts("Invalid index. Please choose a number between 0 and 15.");
        return;
    }

    printf("Enter the size of the note (max 0x2f8): ");
    size = get_uint();
    if (size > MAX_SIZE || size == 0 || size == UINT64_MAX)
    {
        puts("Invalid size. Please choose a size between 1 and 0x2f8.");
        return;
    }

    if (size > UINT16_MAX)
    {
        puts("Size too large for internal representation.");
        return;
    }

    chunks[idx] = malloc(size);
    if (!chunks[idx])
    {
        puts("Memory allocation failed. Please try again.");
        return;
    }

    sizes[idx] = (uint16_t)size;
    puts("Note created successfully!");
}


static void read_note()
{
    uint64_t idx;

    printf("Index of the note (0-%d): ", MAX_NOTE - 1);
    idx = get_uint();
    if (idx >= MAX_NOTE || idx == UINT64_MAX)
    {
        puts("Invalid index. Please choose a number between 0 and 15.");
        return;
    }

    if (chunks[idx] == NULL)
    {
        puts("No note found at this index.");
        return;
    }

    printf("Data: ");
    puts(chunks[idx]);
}


static void edit_note()
{
    uint64_t idx;

    printf("Index of the note (0-%d): ", MAX_NOTE - 1);
    idx = get_uint();
    if (idx >= MAX_NOTE || idx == UINT64_MAX)
    {
        puts("Invalid index. Please choose a number between 0 and 15.");
        return;
    }

    if (chunks[idx] == NULL)
    {
        puts("No note found at this index.");
        return;
    }

    printf("Data: ");
    size_t n = read(0, chunks[idx], sizes[idx]);
    chunks[idx][n] = '\0'; // Ensure null-termination
}

static void delete_note()
{
    uint64_t idx;

    printf("Index of the note (0-%d): ", MAX_NOTE - 1);
    idx = get_uint();
    if (idx >= MAX_NOTE || idx == UINT64_MAX)
    {
        puts("Invalid index. Please choose a number between 0 and 15.");
        return;
    }

    if (chunks[idx] == NULL)
    {
        puts("No note found at this index.");
        return;
    }

    free(chunks[idx]);
    chunks[idx] = NULL;
    sizes[idx] = 0;
    puts("Note deleted successfully!");
}

int main(void)
{
    uint64_t choice;

    setup();
    filter();

    while (1)
    {
        menu();
        choice = get_uint();
        switch (choice)
        {
            case 1:
                create_note();
                break;
            case 2:
                read_note();
                break;
            case 3:
                edit_note();
                break;
            case 4:
                delete_note();
                break;
            case 5:
                puts("Exiting SafeNote. Goodbye!");
                exit(EXIT_SUCCESS);
            default:
                puts("Invalid choice. Please select a valid option.");
        }
    }

    return 0;
}
