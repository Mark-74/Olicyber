/**
 * @file challenge.c
 * @author Fabio Zoratti <fabio.zoratti96@gmail.com>
 * @author Nicola Vella
 */


#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>


void initialize() {
  setvbuf(stdin, NULL, _IOLBF, 0);
  setvbuf(stdout, NULL, _IOLBF, 0);
  setvbuf(stderr, NULL, _IOLBF, 0);
}


char righe[][100] = {

  "Con seppie e scampi saltan già",
  "Che bello i pesci",
  "(Le acciughe) in festa",
  "E sotto l'onda, profonda",
  "Nella padella con la pastella",
  "Che fritto misto per noi!",
  "(La lu) na piena",
  "Che baraonda, gioconda",
  "(Perdon) la testa",
  "Stare a guardare",
  "Pepperrepeppè",
  "Ecco che inizia il gran galà",
  "Scampi e orate con me (saltano, danzano)",
  "Splash!",
  "Insieme io e te",
  "È il pesce tromba che sta a suonare",
  "(E poi) la sera",
  "Seppie e acciughe con te (ballano)"

};


#define ARRAYSIZE sizeof(righe)/sizeof(righe[0])



void safe_scanf(int* addr) {
  if (scanf("%d", addr) != 1) {
    puts("Non sono riuscito a convertire in intero il numero.");
    exit(1);
  }
}


void win() {
  char* flag = getenv("FLAG");
  puts("Congratulazioni, hai vinto, eccoti la flag:");
  puts(flag);
}


void store_num(int* vec) {
  int pos = 0, val = 0;
  puts("In che posizione vuoi immagazzinare il numero?");
  safe_scanf(&pos);
  puts("E cosa vuoi scriverci?");
  safe_scanf(&val);
  vec[pos] = val;
  puts("Fatto!");
  return;
}

void load_num(int* vec) {
  int pos = 0;
  puts("Che posizione vuoi leggere?");
  safe_scanf(&pos);
  printf("Ecco il tuo numero: %d\n", vec[pos]);
}



void print_song(int* vec) {
  puts("Scaldate le ugole, BELANDI!");
  for (unsigned int i = 0; i < ARRAYSIZE; i++) {
    puts(righe[vec[i]]);
  }

  int corretto[] = {13, 3, 14, 1, 9, 7, 10, 15, 17, 12, 16, 6, 11, 2, 8, 0, 4, 5};
  int buono = 1;
  for (unsigned int i = 0; i < ARRAYSIZE; i++) {
    if (corretto[i] != vec[i]) {
      buono = 0;
      break;
    }
  }
  if (buono) {
    puts("BELANDI, HAI RISVEGLIATO IL POTERE DEL GABIBBO!");
    exit(0);
  } else {
    puts("Ho cantato una canzone senza senso, ora sono un gabibbo triste");
    puts("https://www.youtube.com/watch?v=vteFRdBmrY4");
  }
}


#define BUFSIZE 1024
void banner() {
  char buf[BUFSIZE];
  size_t re = 0;
  int fd = open("gabibbo.bin", O_RDONLY);

  if (fd < 0) {
    puts("Errore aprendo il banner");
    exit(-1);
  }
  while ((re = read(fd, buf, BUFSIZE)) > 0) {
    write(1, buf, re);
  }
  close(fd);


  puts("Belandi, giovane. Oggi dobbiamo ricostruire la mia canzone preferita.");
  puts("Mi è caduto il foglio con il testo e adesso le strofe non sono più in ordine.");
  puts("I miei fogli sono in questo ordine, aiutami a riordinarli:\n\n");

  for (unsigned int i = 0; i < ARRAYSIZE; i++) {
    puts(righe[i]);
  }
  puts("\n\n");
}

void menu() {
  puts("Cosa vuoi fare?");
  puts("0) Imposta la strofa n-esima");
  puts("1) Guarda ordine impostato");
  puts("2) Canta la canzone");
  printf("> ");
}


int main() {
  initialize();
  banner();

  int vec[ARRAYSIZE] = {0};
  int choice = 0;


  for (int i = 0; i < 100; i++) {
    menu();
    safe_scanf(&choice);
    switch (choice) {
    case 0:
      store_num(vec);
      break;
    case 1:
      load_num(vec);
      break;
    case 2:
      print_song(vec);
      break;
    case 7:
      i = 100;
      break;
    default:
      puts("Non ho capito");
      break;
    }
  }

  return 0;
}
