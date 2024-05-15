#include<stdio.h>
#include<stdlib.h>

int main(){

	int seed = 0;
	char password[255];

	srand(seed);
	for(int i = 0; i < 255; i++){

	password[i] = (char)(rand() %25 + 65);

	}

	printf("%s", password);

}
