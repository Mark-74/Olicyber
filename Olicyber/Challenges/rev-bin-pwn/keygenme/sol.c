//gcc sol.c -o sol

#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

void pairStrings(char *a1, char *a2, char *a3, int a4)
{
    int v4;
    char *v5;
    int v6;
    int v7;
    int v10 = 0;
    int v11 = 0;
    int v12 = 0;
    while (1)
    {
        if (v11 >= a4)
        {
            if ((int)v12 >= a4)
                break;
        }
        if ((v10 & 1) != 0)
        {
            v4 = v12++;
            v5 = (v4 + a3);
        }
        else
        {
            v7 = v11++;
            v5 = (v7 + a2);
        }
        v6 = v10++;
        *(a1 + v6) = *v5;
    }
}

int main(int argc, char *argv[]) //send user-id as argument
{
    char v4[32];
    strncpy(v4, argv[1], 32);

    char s1[64];
    pairStrings(s1, v4 + 18, v4 + 9, 8);
    pairStrings(s1 + 16, v4, v4 + 18, 8);
    pairStrings(s1 + 32, v4 + 9, v4, 8);
    *(s1 + 48) = 0;

    printf("%s\n", s1);

    return 0;
}