/**
 * Jason W. Monroe
 * jason@jasonmonroe.com
 * 
 * May 20, 2003
 *
 * war.c
 * 
 */
#pragma page()

#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

/* these are the characters that will be used as pixels on the screen */
#define WATER	'~'
#define AX_SHIP	'.'
#define AL_SHIP	'|'
#define MISS	'O'
#define HIT		'*'
#define BORDER	'-'
#define AL		"Ally"
#define AX		"Axis"

#define INIT		-1	/* initial value of ship position */
#define	MIN			0	/* minimum value on grid */
#define MAXP		2	/* maximum number of players */
#define MAXSHIPS	5	/* maximum number of ships */
#define MAXSIZE		5	/* maximum size a ship can be */
#define DIRS		8	/* maximum number of directions a ship can face */
#define STRLEN		10	/* length of a string */
#define HALF		12	/* half the grid */
#define MAXHITS		15	/* maximum number of hits a team can be hit */
#define YMAX		25	/* maximum size of grid on y axis */
#define XMAX		50	/* maximum size of grid on x axis */

/************************* GLOBAL VARIABLES *********************************
value_t			 -int-    value for each ship
dirs_t			 -int-    value for each direction
warGrid			 -char**- actual grid with characters
radarGrid		 -char**- radar grid, that each team can see
x				 -int*-   array to hold x values for each player 
y				 -int*-   array to hold y values for each player
dir				 -int*-   array to hold direction values for each player
i			     -int-    loop control variable
posNo			 -int-    loop control variable
p				 -int-	  represents player number
changeDir		 -int-	  boolean value to change direction
numPlayers       -int-    number of players playing
randNo           -int-    random number selected to generate another number
numAlly			 -int-    number of ally hits
numAxis		     -int-	  number of axis hits
accuracy     	 -int**-  determines how accurate a human is compared to a computer
compChooseCoords -int-    option to determine if human/computer chooses ships position
******************************************************************************/
typedef enum {raft, ptBoat, cruiser, destroyer, carrier} value_t;
typedef enum {n, ne, e, se, s, sw, w, nw} dirs_t;
enum {false, true};
char warGrid[YMAX][XMAX], radarGrid[YMAX][XMAX];
value_t v;
int x[MAXP],y[MAXP], dir[MAXP];
int i,posNo, p, compChooseCoords, changeDir = false;
int numPlayers, randNo, numAlly, numAxis;
int accuracy[MAXP][MAXHITS];

/**** global structs ******/
typedef struct coord
{
	int x, y;
} coord_t;

typedef struct ships
{
	int size;
	coord_t pos[MAXSIZE]; 
	dirs_t dir;
} ships_t;

typedef struct navy
{
	int hits, misses, numturns;
	ships_t ship[MAXSHIPS];
	char name[STRLEN];
} navy_t;
navy_t *player[MAXP];
coord_t temp, attack, random, pick;
/******* prototypes *******/
void count();
void banner();
void createGrid();
void viewGrid();
void addShips();
void initShips();
int checkSpace();
void setOptions();
void pickCoord();
void clearPos();
void chooseCoords();
int checkForWinner();
void playGame();
void gameOver(int);
void tally();
void togglePlayer();

/**************************/
#pragma page()
int main(void)
{
	banner();
	createGrid();
	setOptions();
	initShips();
	chooseCoords();
	count();
	viewGrid();
	playGame();
/*	viewGrid();*/
	tally();
	return(0);
}

/*****************************************************
banner()
prints the banner information
*****************************************************/
#pragma page()
void banner()
{
	printf("*********\n");
	printf("** WAR **\n");
	printf("*********\n\n");
	
	printf("war.c\nCreated by Jason W. Monroe.  JWM Productions.\n");
	printf("http://www.missouri.edu/~jwmfc9\n");
	printf("All Rights Reserved.\n\n\n");

	fflush(stdout);
	return;
}

/*****************************************************
clearPos()
clears the position if a unavailable space is selected.
*****************************************************/
#pragma page()
void clearPos()
{
	player[p]->ship[v].pos[posNo].x = INIT;
	player[p]->ship[v].pos[posNo].y = INIT;

	return;
}

/*****************************************************
togglePlayer()
toggles the players
*****************************************************/
#pragma page()
void togglePlayer()
{
	switch(p)
	{
		case 0: p++;
			break;

		case 1: p--;
			break;

		default: printf("Error in toggling");
			break;
	}

	return;
}

/*****************************************************
createGrid()
creates the grids for the radar and war
*****************************************************/
#pragma page()
void createGrid()
{
	for (temp.y=MIN; temp.y<YMAX; temp.y++)
		for (temp.x=MIN; temp.x<XMAX; temp.x++)
			radarGrid[temp.y][temp.x] = warGrid[temp.y][temp.x] = WATER;
	
	for (temp.x=MIN; temp.x<XMAX; temp.x++)
		radarGrid[HALF][temp.x] = warGrid[HALF][temp.x] = BORDER;
		 
	return;
}

/*****************************************************
viewGrid()
prints the grid
*****************************************************/
#pragma page()
void viewGrid()
{
	printf("\n\n");
	printf("x->\t0    5    1    5    2    5    3    5    4    5\n");
	for (temp.y=MIN; temp.y<YMAX; temp.y++)
		for (temp.x=MIN; temp.x<XMAX; temp.x++)
		{
			if (temp.x == MIN)
				printf("%d\t", temp.y);

			printf("%c", radarGrid[temp.y][temp.x]);	
			/*printf("%c", warGrid[temp.y][temp.x]);*/
			
			if (temp.x == (XMAX-1))
				printf("\n");
		}

	printf("x->\t0    5    1    5    2    5    3    5    4    5\n");
	printf("\n\n");
	
	fflush(stdout);
	return;
}

/*****************************************************
setOptions()
sets the options for random number, number of players,
and whether players/computers pick the coordinates.
*****************************************************/
#pragma page()
void setOptions()
{
	for (p=0; p<MAXP; p++)
		player[p] = (navy_t*)malloc(sizeof(navy_t));

	printf("Select a random number: ");
	scanf("%d*c", &randNo);
/*	randNo = 1;*/
	do
	{
		printf("\nOne or two players: ");
		scanf("%d*c", &numPlayers); 
	/*	numPlayers = 1;*/
	}while(numPlayers > MAXP && numPlayers < 1);

	do
	{
		printf("\nEnter 0 for computer to choose locations, 1 for user to choose: ");
		scanf("%d*c", &compChooseCoords);
	/*	compChooseCoords = 0;*/
	}while(compChooseCoords < 0 || compChooseCoords > 1);

	if (numPlayers == 1)
	{
		printf("\nWould you like to be the \"%s\" or \"%s\"? ", AX, AL);
/*		scanf("%s", player[0]->name);*/
		strcpy(player[0]->name, AL);
		if (strcmp(player[0]->name, AX)==0)
		{
			printf("\nYou are the Axis Powers!\n");
			strcpy(player[1]->name, AL);
		}
		if (strcmp(player[0]->name, AL)==0)
		{
			printf("\nYou are the Allied Powers!\n");
			strcpy(player[1]->name, AX);
		}
	}
	else if (numPlayers == 2)
	{
		printf("\nPlayer 1, would you like to be the \"%s\" or \"%s\"? ", AX, AL);
		/*scanf("%s", player[0]->name);*/
		strcpy(player[0]->name, AL);
		if (strcmp(player[0]->name, AX)==0)
		{
			printf("\nPlayer 1 is the Axis Powers, Player 2 is the Allied Powers\n");
			strcpy(player[1]->name, AL);
		}
		if (strcmp(player[0]->name, AL)==0)
		{
			printf("\nPlayer 1 is the Allied Powers, Player 2 is the Axis Powers\n");
			strcpy(player[1]->name, AX);
		}
	}

	return;
}

/*****************************************************
initShips()
initializes all the players and ships positions, and 
attributes.
*****************************************************/
#pragma page()
void initShips()
{
	for (p=0; p<MAXP; p++)
	{
		player[p]->misses = 0;
		player[p]->hits = 0;
		player[p]->numturns = 0;
		for (v=0; v<MAXSHIPS; v++)
		{
			player[p]->ship[v].dir = INIT;
			player[p]->ship[v].size = v+1;
			for (posNo=0; posNo<player[p]->ship[v].size; posNo++)
			{
				player[p]->ship[v].pos[posNo].x = INIT;
				player[p]->ship[v].pos[posNo].y = INIT;
			}
		}
	}

	return;
}

/*****************************************************
chooseCoords()
choose coordinates for each ship.
*****************************************************/
#pragma page()
void chooseCoords()
{
	switch(compChooseCoords)
	{
		case 0:
			for (v=0; v<MAXSHIPS; v++)
				pickCoord();
			break;
		
		case 1:
			printf("\nPick a coordinate (x,y) on the grid to place the head of your ships.\n");
			printf("The Grid is 50x25 (XxY)\n");
			printf("Pick clockwise which direction you want the ship to face.\n");
			printf("N (%d), NE (%d), E (%d), SE (%d)\n", n,ne,e,se);
			printf("S (%d), SW (%d), W (%d), NW (%d)\n", s,sw,w,nw);
			printf("Input should look like this: x y direction\n");
			fflush(stdout);
			for (v=0; v<MAXSHIPS; v++)
				pickCoord();
			break;

		default: printf("compChooseCoords can only be %d or %d!\n", false, true);
			break;
	}
	
	return;
}

/*****************************************************
addShips()
adds all the ships to the grid
*****************************************************/
#pragma page()
void addShips()
{	/* allies should be on top, axis on bottom */
	for (posNo=0; posNo<player[p]->ship[v].size; posNo++)
	{
		switch(p)
		{
		case 0:
			if (strcmp(player[0]->name, AL)==0)
				warGrid[player[p]->ship[v].pos[posNo].y][player[p]->ship[v].pos[posNo].x] = AL_SHIP;
			else if (strcmp(player[0]->name, AX)==0)
				warGrid[player[p]->ship[v].pos[posNo].y][player[p]->ship[v].pos[posNo].x] = AX_SHIP;
			break;

		case 1:
			if (strcmp(player[1]->name, AX)==0)
				warGrid[player[p]->ship[v].pos[posNo].y][player[p]->ship[v].pos[posNo].x] = AX_SHIP;
			else if (strcmp(player[0]->name, AL)==0)
				warGrid[player[p]->ship[v].pos[posNo].y][player[p]->ship[v].pos[posNo].x] = AL_SHIP;
			break;

		default: printf("Error: addShips()\n");
			break;
		}
	}

/*	viewGrid();*/
	return;
}

/*****************************************************
pickCoord()
picks coordinates and checks the validity
*****************************************************/
#pragma page()
void pickCoord()
{
	int valid;
	for (i=0; i<MAXP; i++)
	{
		x[i] = INIT;
		y[i] = INIT;
		dir[i] = INIT;
		changeDir = false;
	}

	switch(compChooseCoords)
	{
		case 0:
			for (p=0; p<MAXP; p++)
			{
				changeDir = false;
				do
				{
					for (i=0; i<randNo; i++)
						random.x = rand();
					for (i=0; i<randNo; i++)
						random.y = rand();

					if (changeDir == false)
					{/* only change direction don't change coord */
						x[p] = (random.x % XMAX);
						y[p] = (random.y % HALF);

						if (p == 1)
							do
							{
								y[p] = (rand() % YMAX);
							}while(y[p] <= HALF);
					}

					dir[p] = ((random.x+random.y) % DIRS);
					valid = checkSpace(x[p], y[p], dir[p]);
				}while(valid == false);
				addShips();
			}
			break;

		case 1:/* user picks coords */
			switch(v)
			{
				case raft:
					printf("raft: ");
					break;

				case ptBoat:
					printf("ptBoat: ");
					break;

				case destroyer:
					printf("destroyer: ");
					break;
	
				case cruiser:
					printf("cruiser: ");
					break;

				case carrier:
					printf("carrier: ");
					break;

				default: printf("invalid ship\n");
					break;
			}
				
			changeDir = false;
			do
			{	
				p = 0;
				switch(numPlayers)
				{
					case 1: 
						scanf("%d%d%d*c\n", &x[p], &y[p], &dir[p]);
						if (p == 1)
						{
							for (i=0; i<randNo; i++)
								random.x = rand();
							for (i=0; i<randNo; i++)
								random.y = rand();
							if (changeDir == false)
							{/* only change direction don't change coord */
								x[p] = (random.x % XMAX);
								y[p] = (random.y % HALF);

								if (p == 1)
									do
									{
										y[p] = (rand() % YMAX);
									}while(y[p] <= HALF);
							}
							dir[p] = ((random.x+random.y) % DIRS);
						}
						break;

					case 2:
						for (p=0; p<MAXP; p++)
							scanf("%d%d%d*c\n", &x[p], &y[p], &dir[p]);
						break;

					default: printf("Error: pickCords(), numPlayers\n");
						break;
				}

				valid = checkSpace(x[p], y[p], dir[p]);
				addShips();
				

			}while(valid == false);
			togglePlayer();
							
		default: printf("Invalid in pickCoord() %d\n", compChooseCoords);
		break;
	}
	return;
}

/*****************************************************
checkSpace()
checks the space to see if it's water, if so then place
the cockpit on that space and choose which direction.
*****************************************************/
int checkSpace(int c, int r, int d)
{
	int flag = false;
	
	if (warGrid[r][c] == WATER) /* cockpit */
	{	
		for (i=0; i<=player[p]->ship[v].size-1; i++)
		{
			switch(d)
			{
				case n: /* NORTH */
					if (!(warGrid[r-i][c] == WATER))
					{
						posNo = i;
						clearPos();
						changeDir = true;
						return(flag);
					}
					else
					{
						player[p]->ship[v].pos[i].x = c;
						player[p]->ship[v].pos[i].y = r-i;
						player[p]->ship[v].dir = d;
					}
					break;

				case ne: /* NORTHEAST */
					if (!(warGrid[r-i][c+i] == WATER))
					{
						posNo = i;
						clearPos();
						changeDir = true;
						return(flag);
					}
					else
					{
						player[p]->ship[v].pos[i].x = c+i;
						player[p]->ship[v].pos[i].y = r-i;
						player[p]->ship[v].dir = d;
					}
					break;

				case e: /* EAST */
					if (!(warGrid[r][c+i] == WATER))
					{
						posNo = i;
						clearPos();
						changeDir = true;
						return(flag);
					}
					else
					{
						player[p]->ship[v].pos[i].x = c+i;
						player[p]->ship[v].pos[i].y = r;
						player[p]->ship[v].dir = d;
					}
				break;

				case se: /* SOUTHEAST */
					if (!(warGrid[r+i][c+i] == WATER))
					{
						posNo = i;
						clearPos();
						changeDir = true;
						return(flag);
					}
					else
					{
						player[p]->ship[v].pos[i].x = c+i;
						player[p]->ship[v].pos[i].y = r+i;
						player[p]->ship[v].dir = d;
					}
					break;

				case s: /* SOUTH */
					if (!(warGrid[r+i][c] == WATER))
					{
						posNo = i;
						clearPos();
						changeDir = true;
						return(flag);
					}
					else
					{
						player[p]->ship[v].pos[i].x = c;
						player[p]->ship[v].pos[i].y = r+i;
						player[p]->ship[v].dir = d;
					}
					break;
	
				case sw: /* SOUTHWEST */
					if (!(warGrid[r+i][c-i] == WATER))
					{
						posNo = i;
						clearPos();
						changeDir = true;
						return(flag);
					}
					else
					{
						player[p]->ship[v].pos[i].x = c-i;
						player[p]->ship[v].pos[i].y = r+i;
						player[p]->ship[v].dir = d;
					}
					break;

				case w: /* WEST */
					if (!(warGrid[r][c-i] == WATER))
					{
						posNo = i;
						clearPos();
						changeDir = true;
						return(flag);
					}
					else
					{
						player[p]->ship[v].pos[i].x = c-i;
						player[p]->ship[v].pos[i].y = r;
						player[p]->ship[v].dir = d;
					}
					break;

				case nw: /* NORTHWEST */
					if (!(warGrid[r-i][c-i] == WATER))
					{
						posNo = i;
						clearPos();
						changeDir = true;
						return(flag);
					}
					else
					{
						player[p]->ship[v].pos[i].x = c-i;
						player[p]->ship[v].pos[i].y = r-i;
						player[p]->ship[v].dir = d;
					}
					break;

				default: printf("invalid direction\n");
					flag = false;
					return(flag);
					break;
			}	
		}
		flag = true;		
	}
	return(flag);
}

/*****************************************************
count()
counts the number of ships, points on the board.
*****************************************************/
#pragma page()
void count()
{
	numAlly = numAxis = 0;

	for (temp.y=MIN; temp.y<YMAX; temp.y++)
		for (temp.x=MIN; temp.x<XMAX; temp.x++)
		{
			if (warGrid[temp.y][temp.x] == AX_SHIP)
				numAxis++;
			if (warGrid[temp.y][temp.x] == AL_SHIP)
				numAlly++;
		}

	return;
}

/*****************************************************
checkForWinner()
checks to see if anyone has won.  if the number of hits
is equal to the maximum possible of hits an opponent 
can endure than the game is over.
*****************************************************/
#pragma page()
int checkForWinner()
{
	int flag = false;
	if (player[p]->hits == numAxis || player[p]->hits == numAlly)
		flag = true;
	
	return(flag);
	
}

/*****************************************************
playGame()
plays the game, each team chooses where they want to 
attack.
*****************************************************/
#pragma page()
void playGame()
{
	int winFlag; 
	p = 0;
	do
	{
		/*viewGrid();*/
		player[p]->numturns++;
		printf("Turn: %d, %s attack:\n", player[p]->numturns, player[p]->name);
		do
		{
			printf("x: ");
			for (i=0; i<randNo; i++)
				pick.x = (rand() % XMAX);
			attack.x = pick.x;
			
   			scanf("%d", &attack.x);
   
			printf("y: ");
			for (i=0; i<randNo; i++)
				if (p == 0)
					do
					{
						pick.y = (rand() % YMAX);
					}while(pick.y <= HALF);

				if (p == 1)
					pick.y = (rand() % HALF);
			attack.y = pick.y;
	        scanf("%d", &attack.y);
   
		} while ((attack.x<=MIN && attack.x>XMAX) && (attack.y<=MIN && attack.y>YMAX)); 
		
		switch(p)
		{
			case 0:
				if (strcmp(player[p]->name, AL)==0)
					if (warGrid[attack.y][attack.x] == AX_SHIP)
					{
						radarGrid[attack.y][attack.x] = HIT;
						accuracy[p][player[p]->hits] = player[p]->numturns;
						player[p]->hits++;
					}
					/* can't attack own ship */
					else if (warGrid[attack.y][attack.x] == AL_SHIP)
						printf("Can't attack own ship! Lose turn!\n");
					
				if (strcmp(player[p]->name, AX)==0)
					if (warGrid[attack.y][attack.x] == AL_SHIP)
					{
						radarGrid[attack.y][attack.x] = HIT;
						accuracy[p][player[p]->hits] = player[p]->numturns;
						player[p]->hits++;
					}
					/* can't attack own ship */
					else if (warGrid[attack.y][attack.x] == AX_SHIP)
						printf("Can't attack own ship! Lose turn!\n");
				break;

			case 1:
				if (strcmp(player[p]->name, AL)==0)
					if (warGrid[attack.y][attack.x] == AX_SHIP)
					{
						radarGrid[attack.y][attack.x] = HIT;
						accuracy[p][player[p]->hits] = player[p]->numturns;
						player[p]->hits++;
					}
					/* can't attack own ship */
					else if (warGrid[attack.y][attack.x] == AL_SHIP)
						printf("Can't attack own ship! Lose turn!\n");
			
				if (strcmp(player[p]->name, AX)==0)
					if (warGrid[attack.y][attack.x] == AL_SHIP)
					{
						radarGrid[attack.y][attack.x] = HIT;
						accuracy[p][player[p]->hits] = player[p]->numturns;
						player[p]->hits++;
					}
					/* can't attack own ship */
					else if (warGrid[attack.y][attack.x] == AX_SHIP)
						printf("Can't attack own ship! Lose turn!\n");
				break;

			default: printf("Error: playGame()");
				break;
		}

		if (warGrid[attack.y][attack.x] == WATER)
		{
			radarGrid[attack.y][attack.x] = MISS;
			player[p]->misses++;
		}

		winFlag = checkForWinner();

		togglePlayer();

	}while(winFlag == false);

	gameOver(p);
	return;
}

/*****************************************************
gameOver()
Once the game is over this function will print the winner
*****************************************************/
#pragma page()
void gameOver(int p)
{
	switch(p)
	{
		case 0:
		printf("\n\nGAME OVER! Congratulations! The %s wins!\n", player[1]->name);
		break;

		case 1: 
		printf("\n\nGAME OVER! Congratulations! The %s wins!\n", player[0]->name);
		break;

		default: printf("No winner!\n");
		break;
	}

	/* clear the output buffer */
	fflush(stdout);
	return;
}

/**************************************************/
#pragma page()
void tally()
{
	printf("\n");
	printf("----------------------\n");
	printf("These are the tallies:\n");
	printf("----------------------\n");

	for (p=0; p<MAXP; p++)
	{
		printf("%s:\n", player[p]->name);
		printf("\tHits: %d\n", player[p]->hits);
		printf("\tMisses: %d\n", player[p]->misses);
		printf("\tTurns: %d\n\n", player[p]->numturns);
	}

    printf("Accuracy\n");
	printf("accuracy[p][player[p]->numHits] = player[p]->turn\n");
	for (p=0; p<MAXP; p++)
		for (h=1; h<=15; h++)
			printf("accuracy[%d][%d] = %d\n", p, h, accuracy[p][h]);

	for (p=0; p<MAXP; p++)
		for (h=1; h<15; h++)
		{
			guess[h] = abs(accuracy[p][h] - accuracy[p][h+1]);
			printf("guess[%d] = %d\n", h, guess[h]);
		}

	/* clear the output buffer */
	fflush(stdout);
	return;
}
