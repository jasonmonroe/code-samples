/**
 * Jason W. Monroe
 * jason@jasonmonroe.com
 *
 * musical-chairs.c
 *
 * September 12, 2001.  Revised January 3, 2009.
 *
 * Program that plays musical chairs.  Starts game, players revolve around chairs; when music stops one player is out.
 * Utilizes linked lists.
 */

#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>

typedef struct musicalChairs
{
	int no;
	struct musicalChairs *next;
} partic_t;

typedef struct posStruct
{
	partic_t *rear, *front;
} pos_q;

/* prototypes */
void banner(void);
void createList(pos_q *, int);
void playGame(pos_q *, int);
void deleteList(pos_q *);
void printResults(pos_q *);

int main(void)
{
	int i, numPlayers;
	pos_q *player;

	player = (pos_q*)malloc(sizeof(pos_q));
	
	numPlayers = 5;

	for (i=0; i<numPlayers; i++)
		createList(player, i);

	player->front = player->rear->next;
	playGame(player, numPlayers);
	printResults(player);

	return(0);
}

void banner(void)
{
	printf("**********************\n");
	printf("*** MUSICAL CHAIRS ***\n");
	printf("**********************\n\n");
	
	/* clear output buffer */
	fflush(stdout);

	return;
}

void createList(pos_q *player, int i)
{
	partic_t *person;

	person = (partic_t*)malloc(sizeof(partic_t));
	person->no = i;

	printf("[%d]->", person->no);
	if (player->rear == NULL)
	{
		player->rear = person;
		player->rear->next = person;
	}
	else
	{
		person->next = player->rear->next;
		player->rear->next = person;
		player->rear = person;
	}
	
	return;
}

void playGame(pos_q *player, int numPlayers)
{
	int i, randNo;
	
	while(player->front->next != player->front->next->next)
	{
		randNo = rand() % numPlayers;

		for (i=0; i<randNo; i++)
			player->front = player->front->next;

  		// after a random value is picked traverse to the (rand) player and delete
		deleteList(player);
	}
	printf("\n");

	return;
}

void deleteList(pos_q *player)
{
	partic_t *loser;
	
	loser = (partic_t *)malloc(sizeof(partic_t));
	loser = player->front->next;

	/* connects the first node with the third */
	player->front->next = player->front->next->next;

	loser = NULL;
	free(loser);

	return;
}

void printResults(pos_q *player)
{
	printf("****************************************\n");
	printf("* The winner of MUSICAL CHAIRS is [%d] *\n", player->front->no);
	printf("****************************************\n");

	/* clear output buffer */
	fflush(stdout);

	return;
}