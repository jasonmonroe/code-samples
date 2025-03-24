"""
|--------------------------------------------------------------------------
| Weighted Score System
|--------------------------------------------------------------------------
| This is a system where you rank the candidates in order of preference.
| first place votes are weighted by 1, second place votes are weighted by 1/2,
| third place votes are weighted by 1/3, and fourth place votes are weighted by 1/4.
| Multiply the number of votes by the weight and add them up to determine the
| winner.
|
| Note: No candidates are eliminated until the final round.
"""

from helpers import map_id_to_candidate_index, sort_candidates, FIRST_CHOICE_INDEX, show_output
from voting_sys import VotingSystem

class WeightedScoreSystem(VotingSystem):
    def __init__(self, candidates, ballots):
        super().__init__(candidates, ballots) # constructor of parent class
        self.title = 'Weighted Score'

        # Define weighted choice values for each place.
        self.choice_vals = [
            1,     # 1st Place
            1 / 2, # 2nd Place
            1 / 4, # 3rd Place
            1 / 8  # 4th Place
        ]

        self.show_banner()

    def score_ballots(self):
        """
        Score candidate points based on votes ranked by choice.
        """

        for i in range (0, len(self.candidates)):
            self.candidates[i].total = 0

            for j in range (0, len(self.choice_vals)):
                self.candidates[i].total += self.candidates[i].votes[j] * self.choice_vals[j]

            print(f'Candidate: {self.candidates[i].id} Total: {self.candidates[i].total}')
