/**
 * Jason Monroe
 * jason@jasonmonroe.com
 *
 * Oct 8, 2009
 * 
 * Creates a user prompt script for questions and answers and scores at the end.
 */
 
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <malloc.h>

#define DEFLEN 300
#define ANSLEN 15
#define NUMVOCAB 30
#define NUMCHAPS 8

#define QUIT 'q'

int i, chap[NUMCHAPS], option, corrCtr=0, inCorrCtr=0, no=1, randNo, corrFlag=0, *corrArr, *inCorrArr, *randArr;
char myAns[15];
char def[NUMCHAPS][NUMVOCAB][DEFLEN], ans[NUMCHAPS][NUMVOCAB][ANSLEN];

/* prototypes */
void db(void);
void banner(void);
void selectChap(void);
void dispVocab(void);
void results(void);

int main(void)
{
	db();
	banner();
	/* quit command */
	selectChap();
	dispVocab();
	results();
	return(0);
}

void banner(void)
{
	printf("*****************\n");
	printf("*** UNIX CODE ***\n");
	printf("*****************\n\n");

	/* clear output buffer */
	fflush(stdout);

	return;
}

void selectChap()
{
	printf("[0] Chapter  2: UNIX FOR NONPROGRAMMERS\n");
	printf("[1] Chapter  3: THE UNIX SHELLS\n");
	printf("[2] Chapter  6: THE C SHELL \n");
	printf("[3] Chapter  7: UTILITIES\n");
	printf("[4] Chapter  8: NETWORKING\n");
	printf("[5] Chapter 10: WINDOWING SYTEMS\n");
	printf("[6] Chapter 11: C PROGRAMMING TOOLS\n");
	printf("[7] Chapter 12: SYSTEMS PROGRAMMING\n");

	/* clear input buffer */
	fflush(stdin);

	scanf("%d", &option);

	return;
}

void db(void)
{
	/* store max vocab terms for each option */
	chap[0] = 25;
	chap[1] = 13;
	chap[2] = 28;
	chap[3] = 0;
	chap[4] = 0;
	chap[5] = 0;
	chap[6] = 0;
	chap[7] = 0;

	/* chapter 2 */
	/* store definition for each vocab */
	strcpy(def[0][0], "prints the current working directory.");
	strcpy(def[0][1], "takes its input from standard input of from a list of files and displays them to standard output.");
	strcpy(def[0][2], "lists all of the files in the current working directory.");
	strcpy(def[0][3], "allows you to scroll through a lost of files, one page at a time.");
	strcpy(def[0][4], "works just like \"more\", except that it clears the screen before displaying each page.");
	strcpy(def[0][5], "displays the first n lines of a file.");
	strcpy(def[0][6], "displays the last n lines of a file.");
	strcpy(def[0][7], "renames oldfilename as newfilename.  The second form allows you to move a collection of files to a directory.");
	strcpy(def[0][8], "creates a directory.");
	strcpy(def[0][9], "changes a shell's current working directory to be \"directoryname.\"");
	strcpy(def[0][10], "copies contents of \"oldfilename\" to \"newfilename\".");
	strcpy(def[0][11], "removes all of the directories in the list of directory names provided in the command.");
	strcpy(def[0][12], "removes a file's label from the directory hierarchy.");
	strcpy(def[0][13], "prints the named files(s) to the printer specified by the -d option.");
	strcpy(def[0][14], "displays the status of all print jobs sent to any printer.");
	strcpy(def[0][15], "removes all of the specified jobs from the printer queue.");
	strcpy(def[0][16], "counts the number of ines, words, and/or characters in a list of files.  If no files are specified, standard input is used instead.");
	strcpy(def[0][17], "attempts to describe the contents of the filename.");
	strcpy(def[0][18], "displays a list of all of the groups that you are a member of.");
	strcpy(def[0][19], "allows a user to change the group of files that he/she owns.");
	strcpy(def[0][20], "changes the modes of the specified files according to the change parameters.");
	strcpy(def[0][21], "allows a super-user to change the ownership of files.");
	strcpy(def[0][22], "when invoked with a group name as an argument, creates a new shell with an effective group ID corresponding to the gruop name.");
	strcpy(def[0][23], "determines your terminal\'s type and then resets it for standard operation.");
	strcpy(def[0][23], "allows you to examnie and set a terminal\'s characteristics.");

	/* store each answer for each vocab */
	strcpy(ans[0][0], "pwd");
	strcpy(ans[0][1], "cat");
	strcpy(ans[0][2], "ls");
	strcpy(ans[0][3], "more");
	strcpy(ans[0][4], "page");
	strcpy(ans[0][5], "head");
	strcpy(ans[0][6], "tail");
	strcpy(ans[0][7], "mv");
	strcpy(ans[0][8], "mkdir");
	strcpy(ans[0][9], "cd");
	strcpy(ans[0][10], "cp");
	strcpy(ans[0][11], "rmdir");
	strcpy(ans[0][12], "rm");
	strcpy(ans[0][13], "lp");
	strcpy(ans[0][14], "lpstat");
	strcpy(ans[0][15], "cancel");
	strcpy(ans[0][16], "wc");
	strcpy(ans[0][17], "file");
	strcpy(ans[0][18], "groups");
	strcpy(ans[0][19], "chgrp");
	strcpy(ans[0][20], "chmod");
	strcpy(ans[0][21], "chown");
	strcpy(ans[0][22], "newgrp");
	strcpy(ans[0][23], "tset");
	strcpy(ans[0][24], "stty");
	
	/* chapter 3 */
	strcpy(def[1][0], "allows you to change your default login shell.");
	strcpy(def[1][1], "built-in shell command that displays all of its arguments to standard output.");
	strcpy(def[1][2], "copies its standard input to the specified files and to its standard output.");
	strcpy(def[1][3], "generates a listing of process-status information.");
	strcpy(def[1][4], "sleeps for the specified number of seconds and then terminates.");
	strcpy(def[1][5], "executes command and makes it immune to the hangup and terminate signals.");
	strcpy(def[1][6], "terminates a process.");
	strcpy(def[1][7], "causes the shell to suspend until the child process with the specified process ID number terminates.");
	strcpy(def[1][8], "terminates the shell and returns the value number to its parent process.");
	strcpy(def[1][9], "executes the output of command as a regular shell command.");
	strcpy(def[1][10], "causes the shell\'s image to be replaced with comand in the process\' memory space.");
	strcpy(def[1][11], "causes all of the positional paramaters to be renamed.");
	strcpy(def[1][12], "sets the shell\'s unmask value to the specified octal number or displays the current unmask value if the argument is omitted.");

	strcpy(ans[1][0], "chsh");
	strcpy(ans[1][1], "echo");
	strcpy(ans[1][2], "tee");
	strcpy(ans[1][3], "ps");
	strcpy(ans[1][4], "sleep");
	strcpy(ans[1][5], "nohup");
	strcpy(ans[1][6], "kill");
	strcpy(ans[1][7], "wait");
	strcpy(ans[1][8], "exit");
	strcpy(ans[1][9], "eval");
	strcpy(ans[1][10], "exec");
	strcpy(ans[1][11], "shift");
	strcpy(ans[1][12], "unmask");

	/* chapter 7 */
	strcpy(def[2][0], "allows you to search for a pattern in a list of files.  If no files are specified, it searches standard input instead.");
	strcpy(def[2][1], "allows you to search for a pattern in a list of files, but only for fixed strings.");
	strcpy(def[2][2], "allows you to search for a pattern in a list of files, but supports extended regular expressions.");
	strcpy(def[2][3], "displays its input file with all adjacent repeated lines collapsed to a single occurrence of the repeated line.");
	strcpy(def[2][4], "sorts lines in one or more files based on a sorting criteria.");
	strcpy(def[2][5], "tests two files for equality.");
	strcpy(def[2][6], "compares two files and outputs a description of their differences.");
	strcpy(def[2][7], "allows you to save directory structures onto a single backup volume.");
	strcpy(def[2][8], "allows you to save directory structures onto a single backup volume, specifically designed to save files onto tape, so it always archives files onto the end of the storage medium.");
	strcpy(def[2][9], "allows you to save a file system onto multiple backup volumes.");
	strcpy(def[2][10], "allows you to restore a set of files from a previous dump file.");
	strcpy(def[2][11], "recursively descends through filepaths and applies an expression to every file.");
	strcpy(def[2][12], "allows you to schedule a series of jobs to be executed on a periodic basis.");
	strcpy(def[2][13], "allows you to schedule jobs to be executed on a one-time basis.");
	strcpy(def[2][14], "scans the lines of its input and performs actions on every line that matches a particular criteria.");
	strcpy(def[2][15], "creates hard links or symbolic (soft) links to existing files.");
	strcpy(def[2][16], "creates a subshell owened by another user.");
	strcpy(def[2][17], "enables and disables instant mail notification.");
	strcpy(def[2][18], "replaces a file by its compressed version, appending a \"Z\" suffix to the file\'s name.");
	strcpy(def[2][19], "reverses compress and recreates the original file.");
	strcpy(def[2][20], "creates a key-encodes version of a text file.");
	strcpy(def[2][21], "edits an input stream acording to a script that contains editing commands.");
	strcpy(def[2][22], "maps the characters in a file from the one character set to another.");
	strcpy(def[2][23], "transforms underline characters in its input so that they will display correctly on the specified terminal.");
	strcpy(def[2][24], "displays the contents of filename.");
	strcpy(def[2][25], "allows you to \"splice\" a devices file system into the root hierarchy.");
	strcpy(def[2][26], "displays the owner of the shell.");
	strcpy(def[2][27], "displays the pathname of your terminal.");
	
	strcpy(ans[2][0], "grep");
	strcpy(ans[2][1], "fgrep");
	strcpy(ans[2][2], "egrep");
	strcpy(ans[2][3], "uniq");
	strcpy(ans[2][4], "sort");
	strcpy(ans[2][5], "cmp");
	strcpy(ans[2][6], "diff");
	strcpy(ans[2][7], "cpio");
	strcpy(ans[2][8], "tar");
	strcpy(ans[2][9], "dump");
	strcpy(ans[2][10], "restore");
	strcpy(ans[2][11], "find");
	strcpy(ans[2][12], "crontab");
	strcpy(ans[2][13], "at");
	strcpy(ans[2][14], "awk");
	strcpy(ans[2][15], "ln");
	strcpy(ans[2][16], "su");
	strcpy(ans[2][17], "biff");
	strcpy(ans[2][18], "compress");
	strcpy(ans[2][19], "uncompress");
	strcpy(ans[2][20], "crypt");
	strcpy(ans[2][21], "sed");
	strcpy(ans[2][22], "tr");
	strcpy(ans[2][23], "ul");
	strcpy(ans[2][24], "od");
	strcpy(ans[2][25], "mount");
	strcpy(ans[2][26], "whoami");
	strcpy(ans[2][27], "tty");

	strcpy(def[3][0], "");

	strcpy(ans[3][0], "");
	return;
}

void dispVocab(void)
{
	randArr = (int*) malloc(sizeof(int) * chap[option]);
	corrArr = (int*) malloc(sizeof(int) * chap[option]);
	inCorrArr = (int*) malloc(sizeof(int) * chap[option]);
	
	for (i=0; i<chap[option]; i++)
		corrArr[i] = inCorrArr[i] = randArr[i] = 0;

	randNo = (rand() % chap[option]);
	do
	{
		/* clear input buffer */
		fflush(stdin);

		while(randArr[randNo] == 1)
			randNo = (rand() % chap[option]);

		printf("\n%d. %s\n", no, def[option][randNo]);
		scanf("%s", myAns);	
		randArr[randNo] = 1;

		if (strcmp(ans[option][randNo], myAns) == 0)
		{
			corrArr[corrCtr] = randNo;
			corrCtr++;
			printf("Correct! %d\n", corrCtr);
		}
		else 
		{
			inCorrArr[inCorrCtr] = randNo;
			inCorrCtr++;
			printf("Incorrect! %d\n", inCorrCtr);
		}

		no++;
	}while(no <= chap[option]);
	return;

}
void results(void)
{
	double pct;
	pct = (double)corrCtr/chap[option];
	printf("You got %d correct out of %d.  Your score is %f%\n", corrCtr, chap[option], pct);
	printf("\nCorrect\n-------\n");

	for (i=0; i<corrCtr; i++)
		printf("%s\n", ans[option][corrArr[i]]);

	printf("\nIncorrect\n---------\n");

	for (i=0; i<inCorrCtr; i++)
		printf("%s\n", ans[option][inCorrArr[i]]);

	return;
}
