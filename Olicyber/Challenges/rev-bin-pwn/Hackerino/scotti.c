/**
 * @file scotti.c
 * @author Fabio Zoratti <fabio.zoratti96@gmail.com>
 * @thanks to Nicola Vella per le domande
 * Compile with `gcc -g -Wall -fstack-protector-all -fPIE -pie -o scotti -static scotti.c`
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define QCOUNT 6

void initialize() {
  setvbuf(stdin, NULL, _IOLBF, 0);
  setvbuf(stdout, NULL, _IOLBF, 0);
  setvbuf(stderr, NULL, _IOLBF, 0);
}


int main() {
  initialize();

  puts("Benvenuto a \"Chi vuol essere un Hackerino\". Rispondi \
correttamente alle domande e potrai vincere fino ad un milione di DogeCoin (falsi).");
  char* flag = getenv("FLAG");

  char* line = NULL;
  size_t len = 0;
  ssize_t read = 0;

  FILE* fp = fopen("domande.txt", "r");
  if (fp == NULL) {
    perror("Apertura file con le domande");
    exit(-1);
  }

  int dcount = 0;
  int win = 1;
  while (dcount < QCOUNT) {
    char corr_ans[16];
    if ((read = getline(&line, &len, fp)) == -1) { perror("Leggere file"); exit(-1); }
    printf("\n\nEcco la domanda n%d:\n", dcount + 1);
    fputs(line, stdout);
    printf("Le possibili risposte:\n");
    for (int d = 0; d < 4; d++) {
      if ((read = getline(&line, &len, fp)) == -1) { perror("Leggere file"); exit(-1); }
      fputs(line, stdout);
    }
    if ((read = getline(&line, &len, fp)) == -1) { perror("Leggere file"); exit(-1); }
    strncpy(corr_ans, line, 16);
    printf("La tua risposta? ");
    if ((read = getline(&line, &len, stdin)) == -1) { perror("Leggere stdin"); exit(-1); }
    printf("Hai risposto:\n");
    printf(line);
    if (strncmp(corr_ans, line, 16)) {
      puts("Oh no, hai risposto sbagliato. Niente DogeCoins per te.");
      win = 0;
      break;
    }
    printf("Risposta corretta! Passiamo alla prossima domanda.\n");
    ++dcount;
  }
  free(line);
  line = NULL;

  if (dcount >= QCOUNT && win) {
    printf("Congratulazioni, hai vinto un DogeCoin falso! Scaricalo su https://downloadmoreram.com/\
 inserendo il codice promozionale 'grullo2022'\n");
  }

  return 0;
}
