#include<stdio.h>
#include <stdlib.h>

int main(){
    char str[] = "puppamelo tutto";
    char palle[] = "12345 puppa";
    char *ptr;

    long sus = strtol(str, &ptr, 10);
    printf("%s, %ld", ptr, sus);

    long sus2 = strtol(palle, &ptr, 10);
    printf("%s, %ld", ptr, sus2);

    printf("%s", ptr);
}
