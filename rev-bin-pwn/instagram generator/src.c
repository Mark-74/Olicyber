// gcc -Wall -fno-stack-protector -o intagram_generator src.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void clear(){
    while(getchar() != '\n');
}

int main() {
  setvbuf(stdin, NULL, _IOLBF, 0);
  setvbuf(stdout, NULL, _IOLBF, 0);
  setvbuf(stderr, NULL, _IOLBF, 0);

  char frasi[10][64] = {
    "No Pain No Gain",
    "Non tutte le ciambelle escono col buco",
    "L’unica costante della vita è il cambiamento",
    "Dov'è Bugo?",
    "Il destino mescola le carte e noi giochiamo",
    "Non è tutto oro quel che luccica",
    "Il gioco è bello quando è bello",
    "Chi va a Roma perde la poltrona",
    "La vita è piena di sofferenza, ma almeno poi finisce",
    "Entro. Spacco. Esco. Ciao."
  };

  char system_strings[6][64] = {
    "Ritorna per nuove frasi d'effetto",
    "Ne desideri altre? (s/n)",
    "",
    "\nEcco qua la tua frase d'effetto:\n - %s\n\n",
    "Scegli un numero da 1 a 10 per avere la tua frase:\n> ",
    "Generatore frasi per Instagram v0.1",
  };

  FILE* f = fopen("flag.txt", "r");
  fscanf(f, "%63s", system_strings[2]);
  fclose(f);

  unsigned short choice = 0;
  int index = 0;
  char endchoice;

  puts(system_strings[5]);

  do {
    int result = 0;
    do {
      printf(system_strings[4]);
      result = scanf("%hu", &choice);
      clear();
    } while(result != 1 || choice < 1);

    index = (int)(short) choice - 1;

    printf(system_strings[3], frasi[index]);

    do {
      puts(system_strings[1]);
      result = scanf("%c", &endchoice);
      clear();
    } while(result != 1);

  } while (endchoice == 's');

  puts(system_strings[0]);

}