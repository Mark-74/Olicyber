// gcc -Wall -fno-stack-protector -z execstack -o generatore_poco_casuale src.c

#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>

void randomGenerator(int size) {
  char buf[size];

  printf("\nEcco il numero casuale: %lu\n", &buf);

  do {
    puts("Desideri continuare? (s/n)");
    gets(buf);
    if (buf[0] == 'n') {
      exit(0);
    }
  } while (buf[0] != 's');

  return;
}

int main() {
  srand(time(NULL));
  setvbuf(stdin, NULL, _IOLBF, 0);
  setvbuf(stdout, NULL, _IOLBF, 0);
  setvbuf(stderr, NULL, _IOLBF, 0);
  
  puts("Generatore di numeri casuali v0.1");

  do {
    randomGenerator((rand() % 125)*8);
  } while(1);
}