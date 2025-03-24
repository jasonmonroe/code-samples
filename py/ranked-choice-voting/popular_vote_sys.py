"""
|--------------------------------------------------------------------------
| Popular Vote System
|--------------------------------------------------------------------------
| The popular vote system is a simple system where the candidate with the most
| votes wins.  This is the most basic voting system and is NOT based on rank
| choice.
|
| Note: If there is a tie in the popular vote system, the winner is determined
| by next choice votes.
"""

# Import Libraries
from helpers import FIRST_CHOICE_INDEX, show_output, map_id_to_candidate_index, sort_candidates
from voting_sys import VotingSystem


class PopularVoteSystem(VotingSystem):
    def __init__(self, candidates, ballots):
        super().__init__(candidates, ballots)
        self.title = 'Popular'
        self.show_banner()

    def score_ballots(self):
        """
        Score the ballots for each candidate.

        :return:
        """

        for candidate in self.candidates:
            candidate.total = 0
            candidate.total += sum([ballot[FIRST_CHOICE_INDEX].count(candidate.id) for ballot in self.ballots])
            print(f'Candidate: {candidate.id} Total: {candidate.total}')
