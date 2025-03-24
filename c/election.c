/**
 * Jason Monroe
 * jason@jasonmonroe.com
 * 
 * Oct 8, 2009
 *
 * election.c
 * 
 * This article appeared in the September 2004 issue of wired magazine. Oct 21, 2004.
 * 
 * "The electoral college is broken!"
 * 
 * Solution:
 * Move to a popular vote. And make it count with instant runoffs.
 * In this system, voters rank the candidates in order of preference. If the first
 * "winner" doesn't get 50 percent of the vote, the least favorite candidate is dropped,
 * and those votes go to the voters' next favorite candidate. You do a new count, and
 * repeat the process until someone gets 50 percent. This way votes aren't wasted: If
 * voters don't get their first choice, they get something close - their second or
 * third choice. It also allows third parties to emerge without "spoiling it" for
 * like-minded candidate.
 *
 * @link http://www.wired.com/wired/archive/12.09/idol.html?pg=3
 */
 
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <malloc.h>

#define INIT				-1
#define NOTPICKED		0
#define HALF				.50
#define PICKED			1

#define FIRST_PLACE		1
#define SECOND_PLACE		2
#define MIN_CANDIDATES	4
#define STRLEN			15
#define MAX_VOTERS		100

/* global variables */
typedef struct candidateStruct
{
	int votes[MIN_CANDIDATES+1];
} candidate_t;

typedef struct voterStruct
{
	int choice[MIN_CANDIDATES+1];
} voter_t;

/* global variables */
candidate_t *candidate[MIN_CANDIDATES+1];
voter_t *voter[MAX_VOTERS];

int numVoters, 
	numCandidates, 
	candSize, 
	choiceNo, 
	randNo,
	choice = 1,
	winner,
	lowestVoteCount,
	lowestVoteCand,
	candList[MAX_VOTERS],
	picked[MAX_VOTERS];

double pct;

/* prototypes */
void banner(void);
void initElection(void);
void vote(void);
void countVotes(void);
void determineLoser(void);
int chooseCand(void);
int determineWinner(void);

	
int main(void)
{
	banner();
	initElection();
	vote();
	countVotes();
	determineLoser();

	printf("\n*** RESULTS ***\n");
	printf("The winner of the election is Candidate #%d.\n", winner);
	printf("Candidiate #%d got %d out of %d votes.\n\n", winner, candidate[winner]->votes[FIRST_PLACE], numVoters);

	/* clear input and output buffers */
	fflush(stdin);
	fflush(stdout);

	return(0);
}

/**
 * Print Banner
 */
void banner(void)
{
	printf("**************\n");
	printf("** ELECTION **\n");
	printf("**************\n\n");

	printf("Copyright 2004. \n");
	printf("Created by Jason W. Monroe\n");
	printf("--------------------------\n\n");

	/* clear output buffer */
	fflush(stdout);

	return;
}

/**
 * intitialize all values before the voting process starts
 */
void initElection()
{
	int i, j;

	/* clear input buffer */
	fflush(stdin);

	do
	{
		printf("How many candidates? (2-20) ");
		numCandidates = 4;
				//scanf("%d", &numCandidates);	
		printf("%d", numCandidates);
	}while(numCandidates < 2 && numCandidates > 20);

	do
	{
		printf("\nHow many voters? ");
		numVoters = 10;
				//scanf("%d", &numVoters);
		printf("%d", numVoters);
	}while(numVoters <= 1);

	do
	{
		printf("\nSelect a random number: ");
		randNo = 3;
				//scanf("%d", &randNo);
		printf("%d", randNo);
	} while(randNo < 0);

	printf("\n------------------------------------------\n");

	for (i=1; i<=numVoters; i++)
		voter[i] = (voter_t**)malloc(sizeof(voter_t*));

	for (i=1; i<=numCandidates; i++)
	{
		candidate[i] = (candidate_t*)malloc(sizeof(candidate_t));
		picked[i] = NOTPICKED;
		candList[i] = i; 
	}
	
	for (i=1; i<=numVoters; i++)
		for (j=1; j<=numCandidates; j++)
			voter[i]->choice[j] = INIT;
	
	for (i=1; i<=numCandidates; i++)
		for (j=1; j<=numCandidates; j++)
			candidate[i]->votes[j] = NOTPICKED;

	return;
}

/**
 * voting for candidates.
 */
void vote()
{
	int i, j;

	/* it's permissable that some voters may not vote for every candidate but let's assume that 
	 every voter will cast a vote for every candidate in rank */
	printf("\n*** VOTE ***");
	for (i=1; i<=numVoters; i++)
	{
		printf("\n");
		candSize = numCandidates;	
	
		for (j=1; j<=numCandidates; j++)
		{
			candList[j] = j;
			picked[j] = NOTPICKED;		
		}
		for (j=1; j<=numCandidates; j++)
		{
			voter[i]->choice[j] = chooseCand();
			printf("Voter #%d: Choice #%d goes for Candidate #%d.\n", i, j, voter[i]->choice[j]);
		}
	}
	return;
}

/**
 * Choose Candidates by voter choice.
 */
int chooseCand()
{
	int i, j;

	for (i=0; i<=randNo; i++)
		do
		{
			pickAgain:
			choiceNo = (rand() % candSize);
			if (choiceNo == 0)
				choiceNo++;
			if (candList[choiceNo] == INIT)
				goto pickAgain;

		}while(choiceNo <= 0);

	picked[choice] = candList[choiceNo];
	candList[choiceNo] = INIT;
	choice++;
	
	for (i=1, j=0; i<=(candSize-choiceNo); i++, j++)
		candList[choiceNo+j] = candList[choiceNo+i];

	if (candList[candSize] != INIT)
		while(candList[candSize] == INIT)
			candSize--;

	candList[candSize] = INIT;
	candSize--;

	return(picked[choice-1]);
}

/**
 * Count the votes of the voters.
 */
void countVotes()
{
	int i, j;

	for (i=1; i<=numVoters; i++)
		for (j=1; j<=numCandidates; j++)
			candidate[voter[i]->choice[j]]->votes[j]++;
	
	printf("\n*** TALLY ***");
	
	for (i=1; i<=numCandidates; i++)
	{
		printf("\n");
		for (j=1; j<=numCandidates; j++)
			printf("Candidate #%d got %d\t%dplace vote(s).\n", i, candidate[i]->votes[j], j);	
	}

	return;
}

/**
 * Determines who the winner is based on how they placed with first place votes.
 */
int determineWinner()
{
	int i = 1, wFlag = 0;

	/* if any candidate gets more than half of first place votes, we have a winner */
	while(wFlag != PICKED && i <= numCandidates)
	{
		pct = (double)candidate[i]->votes[FIRST_PLACE] / numVoters;
		if (pct > HALF)
		{
			winner = i;
			wFlag = PICKED;
		}
		
		else wFlag = NOTPICKED;
		i++;
	}
	
	return(wFlag);
}

/**
 * Declares the winner by eliminating the bottom candidates.
 */
void determineLoser()
{
	int i, j;

	/* while there is no clear winner, determine who has the lowest vote count, remove candidate
	and add their votes to the voters second choice */
	while(determineWinner() == 0)
	{	
		/* add a vote to seperate candidates from themselves */
		lowestVoteCount = candidate[FIRST_PLACE]->votes[FIRST_PLACE] + 1;
		for (i=1; i<=numCandidates; i++)
			if (candidate[i]->votes[FIRST_PLACE] < lowestVoteCount)
			{
				lowestVoteCand = i;
				lowestVoteCount = candidate[i]->votes[FIRST_PLACE];
			}	
			
			/* check for lowest who got more second place votes between the candidates? */
			else if (candidate[i]->votes[FIRST_PLACE] == lowestVoteCount)
				if (candidate[i]->votes[SECOND_PLACE] < candidate[i-1]->votes[SECOND_PLACE])
				{
					lowestVoteCand = i;
					lowestVoteCount = candidate[i]->votes[FIRST_PLACE];
				} else {
					lowestVoteCand = (i-1);
					lowestVoteCount = candidate[i-1]->votes[FIRST_PLACE];
				}
			
		/* search for voters who gave lowest candidate their first place */
		for (i=1; i<=numVoters; i++)
			if (voter[i]->choice[FIRST_PLACE] == lowestVoteCand)	
				candidate[voter[i]->choice[SECOND_PLACE]]->votes[FIRST_PLACE] += 1;

		/* take lowest votes and give 1st place votes accordingly */	
		free(candidate[lowestVoteCand]);
		candidate[lowestVoteCand] = NULL;
	
		numCandidates--;	
	}	
	return;
}
