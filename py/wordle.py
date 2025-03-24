###
#
# Jason Monroe
# Jul 25, 2024
#
# wordle.py
#
###

# Import random module
import random

class Wordle:

    # Init
    def __init__(self):
        # Constants
        self.MAX_TOTAL_GUESSES = 100
        self.MAX_GUESSES = 6
        self.WORD_LEN = 5
        self.WORD_BANK = []

        self.grid = []
        self.is_game_over = False
        self.guesses = 0
        self.total_guesses = 0
        self.word = ''

    def init_grid(self):
        for i in range(0, self.MAX_GUESSES):
            self.grid[i] = '_____'

    # Load word bank
    def fetch_word_bank(self):
        # @link https://api.frontendexpert.io/api/fe/wordle-words
        self.WORD_BANK = ['HELLO', 'WORLD', 'BINGO', 'WRONG']

    # Pick a random word from the word bank
    def pick_word(self):
        return random.choice(self.WORD_BANK)

    # Is the word in the word bank?
    def is_word_in_bank(self, word):
        if word in self.WORD_BANK:
            return True
        else:
            return False

    # Is word the same as the word to guess
    def is_word_complete(self, word):
        if word == self.word:
            return True
        else:
            return False

    def is_word_partial(self, word):
        return True

    # Is word ascii, 5 letters,
    def is_word_valid(self, word):
        if len(word) == self.WORD_LEN and word.isascii():
            return True
        else:
            return False

    # Show board while playing the game.
    # Board contains: banner grid, and stats
    def show_board(self):
        # Show board
        self.show_banner()

        for row in self.grid:
            print(row)

        self.show_stats()

    # Show banner
    def show_banner(self):
        print('###################')
        print('### W O R D L E ###')
        print('###################')
        print("\n")

    # Show stats of how well you played wordle.
    def show_stats(self):
        print("\n")
        print('Word: ' + self.word)
        print('Guesses: ' + self.guesses + ' of ' + self.MAX_GUESSES)
        print('Total Guesses: ' + self.total_guesses + ' of ' + self.MAX_TOTAL_GUESSES)
        print("\n")

    def update_board(self, word, mode):
        # Determine position by the number of guesses.  Treat guesses like an index.
        pos = self.guesses - 1

        for i in range(0, self.MAX_GUESSES):

            # Assume grid has been initialized with blanks.  We only want to update the grid in the position of the guess.
            # self.grid[i] = '_____'

            # Overwrite the word in the grid if i matches the position.
            if mode == 'complete':
                self.grid[pos] = word.upper()
            elif mode == 'partial':
                # show lower case letters for partial meaning you have the correct letters but in the wrong position.

                self.grid[pos] = self.make_partial_word_string(word)
            else:
                self.grid[pos][i] = word

    def make_partial_word_string(self, word):
        partial_word = ''
        # WORLD v WRONG
        # (picked) self.word = 'WORLD'
        # (input) word = 'WRONG'
        ## letters that match: W, O, R
        ### W is in right pos
        ### R is in wrong pos but in the word
        ### O is in wrong pos but in the word
        # Wro__
        for i in range(0, len(self.word)):
            if word[i] in self.word:
                if word[i] == self.word[i]:
                    partial_word += word[i].upper()
                else:
                    partial_word += word[i].lower()
            #else:
                #partial_word += '_'

        # check if letter is in the word?
            # check if letter is in the right position?

        return partial_word

    # This function actually plays the game.
    def play(self):

        self.init_grid()

        # Show banner
        self.show_banner()

        # Pick a random word from the word bank
        self.word = self.pick_word()

        while self.is_game_over is False or self.guesses < self.MAX_TOTAL_GUESSES:
            # get word
            word = input('(' + self.total_guesses + ') Enter a 5 letter word: ')
            self.total_guesses += 1

            # Check if word is valid
            if self.is_word_valid(word):
                print('Debug: ' + word + 'is valid.')

                if self.is_word_in_bank(word):
                    print('Debug: ' + word + 'is in the word bank.')
                    self.guesses += 1

                    if self.is_word_complete(word):
                        self.is_game_over = True
                        print('Debug: ' + word + 'is complete. Game Over.')
                        self.update_board(word, 'complete')

                    elif self.is_word_partial(word):
                        self.update_board(word, 'partial')
                    else:
                        print('Debug: ' + word + 'is not partial or complete.')
                        self.show_board()
                else:
                    print('Debug: ' + word + 'is not in the word bank.')
            else:
                print('Debug: ' + word + 'is not valid.')

# Play game of Wordle
game = Wordle()
game.play()
game.show_board()
