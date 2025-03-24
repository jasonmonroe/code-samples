/**
 * Jason W. Monroe
 * jason@jasonmonroe.com
 * familytree.c
 * 
 * October 9, 2001. Revised December 9, 2004.
 *
 * Program reads an input file and places each person in a binary tree based on the relationship.  The root is "ME" and everyone else are
 * related to the root user all the way to great-grandparents.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <malloc.h>

#define MAX_ROOTS	10
#define TABLE_SIZE	11
#define STRLEN		15

/* declare relationship constants */
#define SON	"son"
#define DAU	"daughter"
#define BRO	"brother"
#define SIS	"sister"
#define MOT	"mother"
#define FAT	"father"
#define AUN	"aunt"
#define	UNC "uncle"
#define NEP "nephew"
#define NEI	"neice"
#define COU	"cousin"

/* define relation table */
#define TABLE { SON, DAU, FAT, MOT, BRO, SIS, UNC, AUN, NEP, NEI, COU };
//#define TABLE { SON, DAU, FAT, MOT };

#define INP "family-tree\\familytree.txt"
#define TRUE	1

/* declare global variables */
typedef char members[STRLEN];
typedef members table_t[TABLE_SIZE];
table_t table = TABLE;

typedef enum { son, daughter, father, mother, brother, sister, uncle, aunt, nephew, neice, cousin } rel_t;

/* define structs */
typedef struct tree
{
	rel_t relVal;
	members name, rel;
	struct tree *left, *right;
	//struct *paternal, *maternal;
} family_t;

/* prototypes */
void banner(void);
void createTree(family_t **);
rel_t convert(members);
family_t *searchTree(family_t **, int, members);
family_t *preTraverse(family_t *, members);
family_t *insertTree(family_t *, members, members, rel_t);
void defineRel(family_t **, int);
void printOutput(family_t **, int, int, int);

int main(void)
{
	int i, rootCtr = -1, cycle = 0;
	family_t **person, **root, *first, *second;
	members relName, relName2, relStr, relStr2;
	rel_t rel, rel2;
	FILE *inp;
	table_t table = TABLE;

	/* allocate memory for the maximum number of roots */
	person = (struct tree**)malloc(sizeof(struct tree*) * MAX_ROOTS);
	
	/* clear input buffer */
	fflush(stdin);

	/* read file */
	while(fscanf(inp, "%s%s%s%s*c", relName, relStr, relName2, relStr2) != EOF)
	{
		/* get numeric values of relationships */
		rel = convert(relStr);
		rel2 = convert(relStr2);

		/* search the tree to see if the nodes are there, also increment the root counter
		because there will be another root inserted */
		first = searchTree(person, rootCtr+1, relName);
		second = searchTree(person, rootCtr+1, relName2);

		/* check if their son or daughter and if the first pointer exists (at the moment) */
		if (rel < father && first == NULL)
			rootCtr++;

		/* point the person and it's array of roots to the root */
		root = &person[rootCtr];

		/* if first exists than point the first pointer to the root or insert the first node
		into tree */
		if (first)
			root = &first;
		else root[son] = insertTree(root[son], relName, relStr, rel);

		/* if parent exists check if the second relation is the father, store the parent to the left
		side of the root, otherwise set it to the right side (it must be the parent pointers mother */
		if (second)
			if (rel == father || rel2 == father)
				root[son]->left = second;
			else root[son]->rel = second;

		/* else (parent doesn't exist) insert the parents into the tree */
		else root[son] = insertTree(root[son], relName2, relStr2, rel2);
		cycle++;
	}
 
	printf("debug: cycle=%d\n", cycle);

	/* free up the person */
	free(person);
	fclose(inp);
		
	banner();

	return(0);
}

void banner(void)
{
	printf("*******************\n");
	printf("*** FAMILY TREE ***\n");
	printf("*******************\n\n");
	printf("The geneology of the family tree.\n");
	printf("_________________________________\n");

	/* clear output buffer */
	fflush(stdout);
}

void createTree(family_t **person)
{
	/* initialize the list */
	*person = NULL;
}

rel_t convert(members relStr)
{
	/* initialize value when function called */
	rel_t rel = 0;

	/* assign values to the relationships */
	table_t table = TABLE;

	while(strcmp(relStr, table[rel]));
		rel++;

	return(rel);
}

family_t *insertTree(family_t *person, members relName, members relStr, rel_t rel)
{
	/* create new leaf by allocating memory, copy strings into structures, initializing
	their, left and right sides of the tree */
	if (!(person))
	{
		person = (family_t*)malloc(sizeof(family_t));
		strcpy(person->name, relName);
		strcpy(person->rel, relStr);
		person->relVal = rel;
		person->left = person->right = NULL;
	}
	/* check for father, if the fatehr is found of the person, then insert the father to the left side of tree */
	else if (rel == father)
		person->left = insertTree(person->left, relName, relStr, rel);

	/* if not, then it's their mother, so set her to right side of the tree */
	else person->right = insertTree(person->right, relName, relStr, rel);

	/* return the pointer person to main() */
	return(person);
}

family_t *searchTree(family_t **person, int rootCtr, members relName)
{
	/* declare temp pointer */
	family_t *temp;
	int i;
	
	/* for the amout of roots that have been counted traverse the tree that many times.
	store the ponter into the temp pointer */
	for (i=0; i<rootCtr; i++)
	{
		temp = preTraverse(person[i], relName);

		/* if temp exists, return the ponter (that has been traversed) */
		if (temp)
			return(temp);
	}

	return(NULL);
}

family_t *preTraverse(family_t *person, members relName)
{
	/* declare temp pointer */
	family_t *temp;
	
	if (person)
	{
		/* if the name matches go to the root to traverse the tree */
		if (strcmp(person->name, relName) == 0)
			return(person);

		/* recursively traverse the left side of the tree return the poniter into temp */
		temp = preTraverse(person->left, relName);

		/* if the temp is empty, return the pointer to the right side of the tree, otherwise
		return whatever the pointer is */
		if (!(temp)
			return(preTraverse(person->right, relName));
		else return(temp);
	}

	/* if the persno isn't there than return NULL */
	return(NULL);
}

void defineRel(family_t **person, int rootCtr)
{
	int i, j, sameParents, sameGrandParents;
	//table_t table = TABLE;

	/* determine the relatinoships */
	for (i=0, j=1; i<rootCtr, j<(rootCtr+1); i++, j++)
	{
		/* relate each other! compare first root with second root for all possible relations */
		if (strcmp(person[i]->left->name, person[j]->left->name) == 0 && strcmp(person[i]->right->name, person[j]->right->name) == 0)
			sameParents = TRUE;

		/* determine grandparents */
		if (strcmp(person[i]->left->left->name, person[j]->left->left->name) == 0 ||
   			strcmp(person[i]->left->right->name, person[j]->left->right->name) == 0 ||
			strcmp(person[i]->right->left->name, person[j]->right->left->name) == 0 ||
			strcmp(person[i]->right->right->name, person[j]->right->right->name) == 0 ||
			strcmp(person[i]->left->left->name, person[j]->right->left->name) == 0 ||
			strcmp(person[i]->right->left->name, person[j]->left->left->name) == 0)
			sameGrandParents = TRUE;
	}

	/* now that the relationships have been defined print the results */
	printOutput(person, rootCtr, sameParents, sameGrandParents);
}

void printOutput(family_t **person, int rootCtr, int sameParents, int sameGrandParents)
{
	int i, j, k;
	//table_t table = TABLE;
	/* print the roots first */
	printf("The roots for this family are:\n");

	for (i=0; i<rootCtr; i++)
		printf("%s\t", person[i]->name);

	/* determine the relationships */
	for (i=0, j=1; i<rootCtr, j<(rootCtr+1); i++, j++)
	{
		if (sameParents == TRUE)
		{
			/* if two roots have the same parents then they are siblings.  now detrmine their gender to find whether they are brothers or sisters */
			if (person[i]->relVal > person[j]->relVal)
			{
				strcpy(person[i]->rel, table[sister]);
				strcpy(person[j]->rel, table[brother]);
			}
			else if (person[i]->relVal == person[j]->relVal)
			{
				/* check for brothers */
				if (person[i]->relVal == son)
				{
					strcpy(person[i]->rel, table[brother]);
					strcpy(person[j]->rel, table[brother]);
				}
				else /* check for sisters */
				{
					strcpy(person[i]->rel, table[sister]);
					strcpy(person[j]->rel, table[sister]);
				}
			}
			k = i;
		}

		/* determine output if not even related! first check if they have the same dad, if no, 
		then check if they have the same grandfathers then check for great grandparents */
		if (sameParents != TRUE && sameGrandParents != TRUE)
			printf("%s is not related to %s\n", person[i]->name, person[j]->name);

		/* determine cousins, also check for cousin, by comparing the roots grandparents.   
		if they have the same grandparents but not the same paretns then the roots are cousins */
		if (sameParents != TRUE && sameGrandParents == TRUE)
		{
			strcpy(person[i]->rel, table[cousin]);
			strcpy(person[j]->rel, table[cousin]);
			strcpy(person[k]->rel, table[cousin]);
		}

		printf("%s is the %s of %s\n", person[i]->name, person[i]->rel, person[j]->name);
	}

	/* clear input/output buffer */
	fflush(stdin);
	fflush(stdout);
	
	return;
}