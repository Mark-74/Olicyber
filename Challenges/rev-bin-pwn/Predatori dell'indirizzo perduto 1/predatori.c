/**
 * @author Fabio Zoratti <fabio.zoratti96@gmail.com>
 * @author Nicola Vella
 * @file predatori.c
 * Compile with  `gcc -o predatori -static -fstack-protector-all -znoexecstack -Wl,-z,relro predatori.c`
 */

#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>


#define FLAG_SIZE 0x30


#define ERR(msg) \
    do { perror(msg); exit(EXIT_FAILURE); } while (0)


void initialize() {
  setvbuf(stdin, NULL, _IOLBF, 0);
  setvbuf(stdout, NULL, _IOLBF, 0);
  setvbuf(stderr, NULL, _IOLBF, 0);
}



unsigned long long get_num() {
    char buf[24];
    read(STDIN_FILENO, buf, 15);
    return strtoul(buf, NULL, 10);
}



void bputs(char* str) {
  if (*str == '\x00') {
    write(STDOUT_FILENO, "\n", 1);
    return;
  }
  write(STDOUT_FILENO, str, 1);
  bputs(str + 1);
}


void rww() {
  void* dummy2 = NULL;
  void *addr;
  // Non ci saranno BOF quest'oggi
  char dummy[0x38];

  bputs("Indirizzo: ");
  read(STDIN_FILENO, &addr, sizeof(addr));

  bputs("[*] Processo la richiesta...");
  write(STDOUT_FILENO, addr, 8);
}



void www() {
  void* addr = NULL;
  size_t nbytes;
  bputs("Indirizzo: ");
  read(STDIN_FILENO, &addr, sizeof(addr));

  bputs("Quanti bytes: ");
  nbytes = get_num();
  if (nbytes > 8) {
    bputs("Vuoi DDOSsarmi?");
    return;
  }

  bputs("[*] Processando la richiesta...");
  bputs("Cosa vuoi scrivere?");
  read(STDIN_FILENO, addr, 8);
  bputs("Fatto");
}


void motd() {
  char* succ = NULL;
  char buf[0x20];
  bputs("Come si chiama l'attore che interpreta il padre di Indiana Jones, ma che cerca di usare race conditions?");
  succ = fgets(buf, 0x20, stdin);
  if (succ == NULL) {
    ERR("Reading actor");
  }
  if (strstr(buf, "Sean Concurrency")) {
    bputs("Ottima risposta, sei un uomo istruito");
    system("cat flag.txt");
    bputs("https://i.ytimg.com/vi/vf1L8Jsw0QY/mqdefault.jpg");
  } else {
    bputs("Nope, try again");
  }
  return;
}


int main() {
  char flag1_buffer[FLAG_SIZE];
  initialize();
  memset(flag1_buffer, 0, FLAG_SIZE);

  bputs("Benvenuto ai Predatori dell'indirizzo perduto 1.0. Anche se puoi leggere e scrivere dovunque, non otterrai mai /bin/sh");
  bputs("Sto caricando importanti informazioni, mostrerò poi il menù.");

  int fd = open("flag1.txt", O_RDONLY);
  if (fd == -1) {
    ERR("open flag1");
  }
  if (read(fd, flag1_buffer, FLAG_SIZE) == -1) {
    ERR("read flag1");
  }

  int choice;

  for(;;)
    {
      bputs("1) LeggiCosaDove\n2) ScriviCosaDove\n3) Esci");
      choice = get_num();
      switch (choice)
        {
        case 0:
          motd();
          break;
        case 1:
          rww();
          break;

        case 2:
          www();
          break;

        case 3:
          return 0;
        }
    }
}
