/**
 * H file for maze.c.
 * \\maze\maze.h
 *
 * Defines maze grid.
 * Path - Space to move.  0 is closed, 1 is open.
 * Returns status via coordinates.
 * 
 */
typedef struct mazeStruct
{
	int path;
	int exit;
} maze_t;
 
maze_t status;

maze_t grid(int x, int y)
{
	if (x == 0 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 1)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 2)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 3)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 4)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 5)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 6)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 7)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 8)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 9)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 10)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 11)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 12)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 0 && y == 13)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 14)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 15)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 16)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 18)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 0 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 1 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 1 && y == 1)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 2)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 3)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 1 && y == 4)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 5)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 6)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 7)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 8)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 9)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 10)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 11)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 12)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 13)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 14)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 1 && y == 15)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 16)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 1 && y == 18)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 1 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 2 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 2 && y == 1)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 2 && y == 2)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 2 && y == 3)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 2 && y == 4)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 2 && y == 5)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 2 && y == 6)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 2 && y == 7)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 2 && y == 8)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 2 && y == 9)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 2 && y == 10)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 2 && y == 11)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 2 && y == 12)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 2 && y == 13)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 2 && y == 14)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 2 && y == 15)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 2 && y == 16)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 2 && y == 17)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 2 && y == 18)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 2 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 3 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 3 && y == 1)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 3 && y == 2)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 3 && y == 3)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 3 && y == 4)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 3 && y == 5)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 3 && y == 6)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 3 && y == 7)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 3 && y == 8)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 3 && y == 9)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 3 && y == 10)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 3 && y == 11)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 3 && y == 12)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 3 && y == 13)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 3 && y == 14)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 3 && y == 15)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 3 && y == 16)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 3 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 3 && y == 18)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 3 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 4 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 4 && y == 1)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 4 && y == 2)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 4 && y == 3)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 4 && y == 4)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 4 && y == 5)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 4 && y == 6)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 4 && y == 7)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 4 && y == 8)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 4 && y == 9)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 4 && y == 10)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 4 && y == 11)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 4 && y == 12)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 4 && y == 13)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 4 && y == 14)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 4 && y == 15)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 4 && y == 16)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 4 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 4 && y == 18)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 4 && y == 19)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 5 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 5 && y == 1)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 5 && y == 2)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 5 && y == 3)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 5 && y == 4)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 5 && y == 5)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 5 && y == 6)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 5 && y == 7)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 5 && y == 8)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 5 && y == 9)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 5 && y == 10)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 5 && y == 11)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 5 && y == 12)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 5 && y == 13)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 5 && y == 14)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 5 && y == 15)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 5 && y == 16)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 5 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 5 && y == 18)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 5 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 6 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 6 && y == 1)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 6 && y == 2)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 6 && y == 3)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 6 && y == 4)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 6 && y == 5)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 6 && y == 6)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 6 && y == 7)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 6 && y == 8)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 6 && y == 9)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 6 && y == 10)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 6 && y == 11)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 6 && y == 12)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 6 && y == 13)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 6 && y == 14)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 6 && y == 15)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 6 && y == 16)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 6 && y == 17)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 6 && y == 18)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 6 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 7 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 7 && y == 1)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 7 && y == 2)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 7 && y == 3)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 7 && y == 4)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 7 && y == 5)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 7 && y == 6)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 7 && y == 7)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 7 && y == 8)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 7 && y == 9)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 7 && y == 10)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 7 && y == 11)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 7 && y == 12)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 7 && y == 13)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 7 && y == 14)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 7 && y == 15)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 7 && y == 16)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 7 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 7 && y == 18)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 7 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 8 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 8 && y == 1)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 8 && y == 2)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 8 && y == 3)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 8 && y == 4)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 8 && y == 5)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 8 && y == 6)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 8 && y == 7)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 8 && y == 8)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 8 && y == 9)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 8 && y == 10)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 8 && y == 11)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 8 && y == 12)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 8 && y == 13)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 8 && y == 14)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 8 && y == 15)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 8 && y == 16)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 8 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 8 && y == 18)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 8 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 9 && y == 0)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 9 && y == 1)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 9 && y == 2)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 9 && y == 3)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 9 && y == 4)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 9 && y == 5)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 9 && y == 6)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 9 && y == 7)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 9 && y == 8)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 9 && y == 9)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 9 && y == 10)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 9 && y == 11)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 9 && y == 12)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 9 && y == 13)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 9 && y == 14)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 9 && y == 15)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 9 && y == 16)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 9 && y == 17)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 9 && y == 18)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 9 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 10 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 10 && y == 1)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 10 && y == 2)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 10 && y == 3)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 10 && y == 4)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 10 && y == 5)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 10 && y == 6)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 10 && y == 7)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 10 && y == 8)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 10 && y == 9)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 10 && y == 10)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 10 && y == 11)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 10 && y == 12)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 10 && y == 13)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 10 && y == 14)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 10 && y == 15)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 10 && y == 16)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 10 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 10 && y == 18)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 10 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 11 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 11 && y == 1)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 11 && y == 2)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 11 && y == 3)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 11 && y == 4)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 11 && y == 5)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 11 && y == 6)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 11 && y == 7)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 11 && y == 8)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 11 && y == 9)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 11 && y == 10)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 11 && y == 11)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 11 && y == 12)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 11 && y == 13)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 11 && y == 14)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 11 && y == 15)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 11 && y == 16)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 11 && y == 17)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 11 && y == 18)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 11 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 12 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 12 && y == 1)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 12 && y == 2)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 12 && y == 3)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 12 && y == 4)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 12 && y == 5)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 12 && y == 6)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 12 && y == 7)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 12 && y == 8)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 12 && y == 9)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 12 && y == 10)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 12 && y == 11)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 12 && y == 12)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 12 && y == 13)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 12 && y == 14)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 12 && y == 15)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 12 && y == 16)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 12 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 12 && y == 18)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 12 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 13 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 13 && y == 1)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 13 && y == 2)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 13 && y == 3)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 13 && y == 4)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 13 && y == 5)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 13 && y == 6)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 13 && y == 7)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 13 && y == 8)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 13 && y == 9)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 13 && y == 10)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 13 && y == 11)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 13 && y == 12)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 13 && y == 13)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 13 && y == 14)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 13 && y == 15)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 13 && y == 16)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 13 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 13 && y == 18)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 13 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 14 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 14 && y == 1)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 14 && y == 2)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 14 && y == 3)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 14 && y == 4)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 14 && y == 5)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 14 && y == 6)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 14 && y == 7)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 14 && y == 8)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 14 && y == 9)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 14 && y == 10)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 14 && y == 11)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 14 && y == 12)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 14 && y == 13)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 14 && y == 14)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 14 && y == 15)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 14 && y == 16)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 14 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 14 && y == 18)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 14 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 15 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 15 && y == 1)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 15 && y == 2)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 15 && y == 3)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 15 && y == 4)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 15 && y == 5)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 15 && y == 6)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 15 && y == 7)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 15 && y == 8)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 15 && y == 9)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 15 && y == 10)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 15 && y == 11)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 15 && y == 12)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 15 && y == 13)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 15 && y == 14)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 15 && y == 15)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 15 && y == 16)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 15 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 15 && y == 18)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 15 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 16 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 16 && y == 1)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 16 && y == 2)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 16 && y == 3)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 16 && y == 4)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 16 && y == 5)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 16 && y == 6)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 16 && y == 7)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 16 && y == 8)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 16 && y == 9)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 16 && y == 10)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 16 && y == 11)
	{
		status.path = 10;
		status.exit = 0;
	}

	if (x == 16 && y == 12)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 16 && y == 13)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 16 && y == 14)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 16 && y == 15)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 16 && y == 16)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 16 && y == 17)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 16 && y == 18)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 16 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 17 && y == 0)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 1)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 2)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 3)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 4)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 5)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 6)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 7)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 17 && y == 8)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 9)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 10)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 11)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 12)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 17 && y == 13)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 14)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 15)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 16)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 17 && y == 18)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 17 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 18 && y == 0)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 18 && y == 1)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 18 && y == 2)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 18 && y == 3)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 18 && y == 4)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 18 && y == 5)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 18 && y == 6)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 18 && y == 7)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 18 && y == 8)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 18 && y == 9)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 18 && y == 10)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 18 && y == 11)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 18 && y == 12)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 18 && y == 13)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 18 && y == 14)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 18 && y == 15)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 18 && y == 16)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 18 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}
 
	/* END */
	if (x == 18 && y == 18)
	{
		status.path = 1;
		status.exit = 1;
	}

	if (x == 18 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 0)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 19 && y == 1)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 19 && y == 2)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 3)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 4)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 5)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 6)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 7)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 19 && y == 8)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 9)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 10)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 11)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 12)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 13)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 14)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 15)
	{
		status.path = 1;
		status.exit = 0;
	}

	if (x == 19 && y == 16)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 17)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 18)
	{
		status.path = 0;
		status.exit = 0;
	}

	if (x == 19 && y == 19)
	{
		status.path = 0;
		status.exit = 0;
	}

	return(status);
}
