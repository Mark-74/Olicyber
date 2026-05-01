#define _GNU_SOURCE
#include <stdlib.h> 
#include <stdio.h> 
#include <unistd.h>
#include <string.h>
#include <sys/mman.h>

#define min(a, b) ((a) < (b) ? (a) : (b))

#define PTRS_SIZE 0x100
#define SIZE_CAP 0x500

void* ptrs[PTRS_SIZE] = {0};
int sizes[PTRS_SIZE] = {0};

unsigned long* admin = NULL;

void print_banner() {
    printf("🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣\n");
    printf("🎣.__                                         _____  ___________.__       .__    .__                🎣\n");
    printf("🎣|  |__   ____  __ __  ______ ____     _____/ ____\\ \\_   _____/|__| _____|  |__ |__| ____    ____  🎣\n");
    printf("🎣|  |  \\ /  _ \\|  |  \\/  ___// __ \\   /  _ \\   __\\   |    __)  |  |/  ___/  |  \\|  |/    \\  / ___\\ 🎣\n");
    printf("🎣|   Y  (  <_> )  |  /\\___ \\\\  ___/  (  <_> )  |     |     \\   |  |\\___ \\|   Y  \\  |   |  \\/ /_/  >🎣\n");
    printf("🎣|___|  /\\____/|____//____  >\\___  >  \\____/|__|     \\___  /   |__/____  >___|  /__|___|  /\\___  / 🎣\n");
    printf("🎣     \\/                  \\/     \\/                      \\/            \\/     \\/        \\//_____/  🎣\n");
    printf("🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣🎣\n");
}

void setup() {
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);

	admin = (unsigned long*) mmap((void*) 0x1337000, 8, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_FIXED | MAP_ANON, -1, 0);

	print_banner();
}

void menu() {
	puts("1) create");
	puts("2) update");
	puts("3) delete");
	puts("4) copy");
	printf("enter your choice: ");
}

int get_choice() {
	unsigned int choice = 0;
	scanf("%d%*c", &choice);

	return choice;
}

void die(char* msg) {
	printf("wrong %s\n", msg);
	exit(-1);
}

unsigned int get_idx() {
	unsigned int idx;

	printf("enter index: ");
	idx = get_choice();

	if (idx >= PTRS_SIZE) 
		die("index");

	return idx;
}	

unsigned int get_size() {
	unsigned int size;

	printf("enter size: ");
	size = get_choice();
	size += 0xf;
	size /= 0x10;
	size *= 0x10;

	if (size >= SIZE_CAP) 
		die("size");

	return size;
}

void read_exactly(int fd, char* ptr, int size) {
	for (int i=0; i<size; i++)
		read(fd, ptr+i, 1);
}

void create() {
	unsigned int idx;
	unsigned int size;
	void* ptr;

	idx = get_idx();
	size = get_size();

	ptr = malloc(size);
	printf("allocated size: %d\n", size);

	ptrs[idx] = ptr;
	sizes[idx] = size;
}

void update() {
	unsigned int idx;

	idx = get_idx();

	printf("enter %d bytes: ", sizes[idx]);
	read_exactly(STDIN_FILENO, ptrs[idx], sizes[idx]);
}

void delete() {
	unsigned int idx;

	idx = get_idx();
	free(ptrs[idx]);
}	

void win() {
	if (*admin == 0xdeadbeefdeadcafe) {
		puts("good boy");
		system("/bin/sh");
	} else 
		die("admin");
}

void copy() {
	unsigned int dest;
	unsigned int src;

	dest = get_idx();
	src = get_idx();

	memcpy(ptrs[dest], ptrs[src], min(sizes[dest], sizes[src]));
}

int main(int argc, char** argv) {
	unsigned int choice = 0;

	setup();

	while(1) {
		menu();
		choice = get_choice();

		switch(choice) {
			case 1:
				create();
				break;
			case 2:
				update();
				break;
			case 3:
				delete();
				break;
			case 4:
				copy();
				break;
			case 5:
				win();
				break;
			default:
				puts("invalid choice");
				break;
		}
	}

	return 0;
}
