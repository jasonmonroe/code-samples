#pragma page()

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>

#define QUITCOMM 'q'
#define STRLEN 25
#define SIZE 1



/* global variables */
char roomaji[SIZE][STRLEN];
char english[SIZE][STRLEN];
char answer[STRLEN];
int finished=0, correct=0, incorrect=0, ctr = 0, randNo;

/* db */
strcpy(roomaji[0], "tasukete");

strcpy(english[0], "help");


/******/
int main(void)
{
	while(strcmp(*answer, QUITCOMM) != 0) || finished != 1)
		finished = start();
	
	results();
	return(0);
}

int start()
{
	if (ctr == SIZE)
		flag = 1;
	else flag = 0;

	printf("%s", english[randNo]);
	scanf("%s", answer);

	if (strcmp(roomaji[randNo], answer) == 0)
	{
		printf("Correct!\n");
		correct++;
	}
	else
	{
		printf("Incorrect! %s\n", roomaji[randNo]);
		incorrect++;
	}

	ctr++;
	return(flag);
}

void results()
{
	int i;
	percent = correct/incorrect;
	printf("Your score is: %d out of %d for %f %\n", correct, incorrect, percent);
	printf("\nTrivia you got wrong:\n\n");
	
	for (i=0; i<incorrect; i++)
		printf("%s - %s\n", temp, answer);
}
