/**
 * @file challenge.c
 * @author Mario Del Gaudio <mario@athdesk.me>
 * Compile with `make`
 */


#include <stdio.h>
#include <stdlib.h>

void initialize() {
  setvbuf(stdin, NULL, _IOLBF, 0);
  setvbuf(stdout, NULL, _IOLBF, 0);
  setvbuf(stderr, NULL, _IOLBF, 0);
}

char str[] = "\x95\x63\x7f\x9d\x33\xb2\xd9\x57\x3c\xe3\x34\xec\x70\x63\x30\x2c\xb6\x9f\x44\x70\xa0\xbe\x78\xf7\xb9\0";

int main(int argc, char** argv) {
  initialize();
  char* key = ((unsigned long)main - 0x22e) ;

  if (argc < 2) {
    exit(1);
  }

  if (strlen(argv[1]) != 25) {
    exit(1);
  }

  for (int i = 0; i < 25; i++){
    argv[1][i] ^= key[i];
  }

  if (!memcmp(str, argv[1], 25)) {
    puts("Correct!");
  }

  return 0;
}