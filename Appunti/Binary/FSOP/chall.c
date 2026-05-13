#define _GNU_SOURCE
#include <stdio.h>
#include <dlfcn.h>

void init(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(){
  init();
  void *printf_address = dlsym(RTLD_NEXT, "printf");
  void *read_address;
  char name[0x20];

  printf("libc leak:%p\npie leak:%p\n", printf_address, main);

  printf("Where do you want to write? > ");
  scanf("%p%*c", &read_address);

  printf("Insert your name for the record: ");
  fgets(name, 0x20, stdin);

  printf("Insert data at %p: ", read_address);
  fgets(read_address, 0x100, stdin);
  printf("Done, %s.", name);
  return 0;
}
