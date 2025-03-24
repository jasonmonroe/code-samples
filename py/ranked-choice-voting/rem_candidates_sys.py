"""
|--------------------------------------------------------------------------
| Top Remaining Candidates System
|--------------------------------------------------------------------------
| This system is used by the state of Alaska. Instead of choosing one candidate,
| you fill in the oval in column one for the candidate you would most like to win,
| then vote for your second choice in column two and so on.  Ranking other candidates
| does not impact your first choice, and you do not have to rank them all.  You should
| only mark one oval in each row and one oval in each column.
|
| The ballots are tallied and scored by its first choice votes.  If a candidate
| gets at least half of the votes in round one, they win.  If this doesn't happen, it's
| continued to next round and the candidate with the least nth choice votes is eliminated.
| Count the voter's next remaining candidate choice instead of their choice for the
| eliminated candidate (meaning they still have a say in whom wins).
|
| Repeat these steps in rounds until there are only two candidates and now whomever
| has the most votes is determined the winner.

| @link https://www.elections.alaska.gov/election-information/
| @link https://www.youtube.com/watch?v=lLU3lbrxMBI
| @link https://www.youtube.com/watch?v=oHRPMJmzBBw
"""

from helpers import MAX_CHOICES, NO_VOTE_VAL, FIRST_CHOICE_INDEX, map_id_to_candidate_index, sort_candidates, place_str
from voting_sys import VotingSystem

class RemainingCandidatesSystem(VotingSystem):
    def __init__(self, candidates, ballots):
        super().__init__(candidates, ballots)

        self.title = 'Remaining Candidates'
        self.show_banner()

    def recount_ballots(self):
        """
        Count all first place votes to determine winner.
        If no majority, count every voter's next choice votes and add to the total.
        Calculate the majority vote with total ballots * choice value.
        Example: Second round
        voter_cnt = len(self.ballots)

        :param int round_num: The current round number.
        """

        # Reset total points for each candidate so we can count the first choice each round.
        self.reset_candidate_totals()

        for i in range(0, self.voter_cnt):
            ballot = self.ballots[i]

            # Note: since we're removing the loser from the ballot, we only need to count the top row.
            voted_id = ballot[FIRST_CHOICE_INDEX]

            if voted_id != NO_VOTE_VAL:
                index = map_id_to_candidate_index(voted_id, self.candidates)
                self.candidates[index].total += 1
                #print('Round:', round_num, 'Voted ID:', voted_id, 'Total:', self.candidates[index].total)
            else:
                pass
                #print(f'Voter {i} did not vote for {place_str(0, "p")}.')

        #print('\nRound #', round_num)
        #for candidate in self.candidates:
        #    print(f'Candidate: {candidate.id} Total: {candidate.total}')

    def score_ballots(self):
        """
        Score the ballots for each candidate.
        This is the first step in the remaining candidates' system.
        """

        round_num = 1
        self.recount_ballots()

        while self.determine_winner_by_majority(round_num) != True and round_num <= MAX_CHOICES:

            # After tallying "new" totals, if there is still no majority, get the least voted candidate.
            loser = self.determine_loser()

            # Remove loser from candidate pool and from all ballots.
            loser_index = self.candidates.index(loser)
            self.candidates[loser_index].is_winner = False

            # Remove the loser candidate from all the ballots so they are not counted in the next round.
            self.remove_loser_from_ballot(loser)

            round_num += 1
            self.recount_ballots()

        # Order candidates by points descending
        self.candidates = sort_candidates(self.candidates)
