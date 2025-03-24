/**
Jason W. Monroe
jason@jasonmonroe.com

Written November 7, 2001.  Revised November 21, 2009.

maze.c

You have been thrust somewhere in the middle of a maze.  When you enter the maze, you have no idea
where you are nor whre the exit(s) are.  the one toool that allows you to fine your way out is your 
memory.  Once you start moving about the maze to fnid the exits, yo8u are able to remember eveywhere
you have been.

In an attempt to prevent yourself or others from ever landing in the predicament that you are in, you 
decide to fine and record all of the ways out of the maze so that the information can be passed on or 
retained for future use.

Your goal is to find every exit from the mae and print out the path that you took to get ther from your
starting spot.

INDENTIFIER DICTIONARY
x . . . . . . . int . . . . horizontal coordinate
y . . . . . . . int . . . . vertical coordinate
xPrev . . . . . int . . . . previous horizontal coordinate before move
yPrev . . . . . int . . . . previous vertical coordinate before move
pos[400]. . . . pos_t . . . position in grid
dir_t . . . . . dir . . . . numeric direction of position
posCtr. . . . . int . . . . count of the positions moved
visited[20][20] int . . . . grid of where the position has visited
status. . . . . maze_t  . . determines whether the path is open or not

Notes and Assumptions
1.  Assume that if an option is not available that the next option will proceed accordingly to a clockwise direction.
2.  Assume the edges are not necessarily exits.
3.  There can be more than one exit.
4.  For this program Start at X=4, Y=11 and End at X=18, Y=18
***************************************************/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <\\maze\maze\\maze.h>

#define INVALID_DIR 4
#define TBL_SIZE 4
#define STRLEN 6

#define Y_MIN 0
#define X_MIN 0
#define Y_MAX 20
#define X_MAX 20
#define MAX_POS X_MAX * Y_MAX

#define OPEN ' '
#define CLOSED '*'
#define START 'S'
#define END 'E'

#define NORTH "North"
#define SOUTH "South"
#define EAST "East"
#define WEST "West"

#define TABLE {NORTH, EAST, SOUTH, WEST};
typedef enum {North, East, South, West} dir_t;
typedef char str_t[STRLEN];
typedef str_t tbl_t[TBL_SIZE];

typedef struct mazePosStruct
{
	int x, y;
	dir_t dir;
} pos_t;

/*** prototypes ***/
void banner(int, int);
void initGrid(int [][X_MAX], pos_t []);
void move(int x, int y, dir_t dir, int [][X_MAX], pos_t [], int);
void mazeStart(int *, int *);
maze_t grid(int, int);

/* global variables */
tbl_t str_table = TABLE;
int attempts = 0;

int main(void)
{
	/* declare variables and initialize positions */
	pos_t pos[MAX_POS];
	dir_t dir = 0;
	int posCtr = 0, visited[Y_MAX][X_MAX], x, y;
	
	/* initialize position */
	initGrid(visited, pos);

	/* call this function to know what coordinates we are at when we begin the maze */
	mazeStart(&x, &y);
	move(x, y, dir, visited, pos, posCtr);
	
	/* clear output buffer */
	fflush(stdin);
	fflush(stdout);

	return(0);
}

/*******************************************
banner()
prints banner at the start of the program
inputs: xStart, yStart
returns: nothing
*******************************************/
void banner(int xStart, int yStart)
{
	printf("\n");
	printf("**********\n");
	printf("** MAZE **\n");
	printf("**********\n\n");
	printf("START\t(%d,%d)\n", xStart, yStart);
	printf("---------------\n");

	/* clear output buffer */
	fflush(stdout);

	return;
}

/**********************************************
initGrid()
initialized grid to begin maze.
inputs: int visited[20][20], pos_t pos[400]
returns nothing
**********************************************/
void initGrid(int visited[][X_MAX], pos_t pos[])
{
	int x, y;
	for (x=0; x<X_MAX; x++)
		for (y=0; y<Y_MAX; y++)
		{
			visited[y][x] = 0;
			pos[x * X_MAX + y].x = -1;
			pos[x * Y_MAX + y].y = -1;
			pos[x * Y_MAX + y].dir = 0;
		}

	return;
}


/*********************************************
mazeStart()
picks the starting coordinates to being maze.
input: *xStart, *yStart
output: nothing
*********************************************/
void mazeStart(int *x, int *y)
{
	int i, randNo;
	
	printf("Pick random number: ");
	fflush(stdin);
	scanf("%d", &randNo);

	do
	{
		for (i=0; i<randNo; i++)
		{
			*x = (rand() % X_MAX);
			*y = (rand() % Y_MAX);
		}
		status = grid(&x, &y);

	} while(status.path == 1);

	return;
}

/******************************************************
move()
moves position within maze. backtracks when at dead end.
inputs: int x, int y, dir_t dir, int visited[20][20], pos_t pos[400], int posCtr
outputs: nothing
******************************************************/
void move(int x, int y, dir_t dir, int visited[][X_MAX], pos_t pos[], int posCtr)
{
	maze_t status;
	int i, xPrev, yPrev;
	
	/* record movement */
	pos[posCtr].x = x;
	pos[posCtr].y = y;
	visited[y][x] = 1;

	posCtr++;
	status = grid(x, y);

	/* check for exit */
	if (status.exit == 1)
	{
		banner(pos[0].x, pos[0].y);
		for (i=0; i<posCtr-1; i++)
			printf("%s:\t(%d,%d)\n", str_table[pos[i].dir], pos[i+1].x, pos[i+1].y);
		
		printf("\n");
		printf("EXIT (%d,%d)\n\n", pos[posCtr-1].x, pos[posCtr-1].y);

		/* clear output buffer */
		fflush(stdout);

		return;
	}

	/*** go through maze ***/
	while(dir != INVALID_DIR)
	{
		attempts++;
 
		xPrev = x;
		yPrev = y;
		pos[posCtr-1].dir = dir;

		switch(dir)
		{
			case North:
				y++;
				break;

			case East:
				x++;
				break;

			case South:
				y--;
				break;

			case West:
				x--;
				break;
	
			default: printf("Invalid Direction!\n");
				break;
		}

		/* set boundries check if path is open, then use recursion to move to next spot */
		if ((x >= X_MIN && x < X_MAX) && (y >= Y_MIN && y < Y_MAX))
		{
			status = grid(x, y);
			if (status.path == 1)
				if (visited[y][x] == 0)
				{
					dir = North;
					move(x,y, dir, visited, pos, posCtr);
				}

			/* path is blocked, revert to old coordinates and decrement position counter */
			x = xPrev;
			y = yPrev;
			dir++;
		}

		/* out of bounds, change direction */
		else dir++;
	} 

	/* backtrack if all directions have been exhausted */
	posCtr--;

	return;
} 
