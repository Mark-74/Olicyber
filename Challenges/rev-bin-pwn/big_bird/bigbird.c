/**
 * @file bigbird.c
 * Compile with `gcc -no-pie -fstack-protector-all -o bigbird -masm=intel -static bigbird.c`
 */
#include <stdio.h>
#include <stdlib.h>


void win() {
  char buf[128];
  FILE* fp = fopen("flag.txt", "r");
  fread(buf, sizeof(*buf), 128, fp);
  puts(buf);
}


void initialize() {
  setvbuf(stdin, NULL, _IOLBF, 0);
  setvbuf(stdout, NULL, _IOLBF, 0);
  setvbuf(stderr, NULL, _IOLBF, 0);
}

int main() {
  initialize();
  char buf[40];
  asm("mov rsi, [rbp - 0x8]");
  printf("Here, take some data about this BIG BIRD: %p\n");
  puts("Listen to some good music: https://www.youtube.com/watch?v=9Gc4QTqslN4");
  gets(buf);
  puts("Bye");
  return 0;
}
