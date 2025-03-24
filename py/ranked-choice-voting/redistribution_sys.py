"""
|--------------------------------------------------------------------------
| Redistribution System
|--------------------------------------------------------------------------
| If no winner, remove the candidate with the least number of votes.  Then
| for every ballot where the losing candidate was chosen, count the next choice
| votes of the losing candidate and redistribute them to the remaining candidates.
| Continue this process until a candidate receives more than half of the votes
| to determine the winner.
"""

from helpers import map_id_to_candidate_index, sort_candidates, place_str, MAX_CHOICES, NO_VOTE_VAL, FIRST_CHOICE_INDEX
from voting_sys import VotingSystem

class RedistributionSystem(VotingSystem):
    def __init__(self, candidates, ballots):
        super().__init__(candidates, ballots)
        self.title = 'Redistribution'
        self.show_banner()

    def recount_ballots(self, vote_choice):
        """
        Count all first place votes to determine winner.
        If no majority, count every voter's next choice votes and add to the total.

        :param int vote_choice: The current vote choice.
        :return: None
        """

        # Only count votes for candidates that are still in the pool.
        for i in range(0, len(self.candidates)):
            if self.candidates[i].is_winner is None:
                #print('Before -> Candidate', self.candidates[i].id, 'Total:', self.candidates[i].total)
                self.candidates[i].total += self.candidates[i].votes[vote_choice]
                #print('After -> Candidate', self.candidates[i].id, 'Total:', self.candidates[i].total)


    def score_ballots(self):
        """
        Score the ballots for each candidate.
        This is the first step in the redistribution system.

        :return:
        """

        candidate_cnt = len(self.candidates)
        choice_cnt = min(MAX_CHOICES, candidate_cnt)

        self.recount_ballots(FIRST_CHOICE_INDEX)
        vote_choice = FIRST_CHOICE_INDEX

        # Count all first place votes to determine winner.
        while self.determine_winner_by_majority(vote_choice + 1) is not True and vote_choice <= choice_cnt:

            # print(' while() Vote Choice:', vote_choice, ' ')

            # After tallying "new" totals, if there is still no majority, get the least voted candidate.
            loser = self.determine_loser()
            if loser is None:
                break

            #print(' Loser:', loser.id)

            # Apply loser votes to other candidates.
            self.apply_loser_votes_to_other_candidates(loser, vote_choice)

            # Remove loser from candidate pool.
            loser_index = self.candidates.index(loser)
            self.candidates[loser_index].is_winner = False

            # Note: No need to recount ballots as we only count when applying loser votes to other candidates!
            vote_choice += 1

        # Order candidates by points descending
        self.candidates = sort_candidates(self.candidates)

    def apply_loser_votes_to_other_candidates(self, loser, choice):
        """
        Apply the loser's votes to other candidates total points starting with the highest choice.
        Apply the next place votes of the eliminated candidate to the first place of remaining candidates.

        :param obj loser: The candidate that was eliminated.
        :param int choice: The choice that the loser was voted for.

        :return: None
        """

        #print(f'  Applying loser {loser.id}\'s votes to other candidates...')

        next_choice = choice + 1
        #print(f'  Checking ballots for choice {choice}:', self.ballots)
        for i in range (0, len(self.ballots)):
            if self.ballots[i][choice] == loser.id:
                #print(f'   Voter {i} voted for loser {loser.id} at {place_str(choice, "p")}')
                if next_choice < MAX_CHOICES:
                    next_choice_voted_id = self.ballots[i][next_choice]
                    #print('   Next choice is candidate ID:', next_choice_voted_id)

                    if next_choice_voted_id != NO_VOTE_VAL:
                        next_choice_index = map_id_to_candidate_index(next_choice_voted_id, self.candidates)

                        # Only apply losing votes to candidates that are still in the pool
                        if self.candidates[next_choice_index].is_winner is None and self.candidates[next_choice_index].id != loser.id:
                            self.candidates[next_choice_index].total += 1
                            #print(f'   Voter {i} next choice went to {self.candidates[next_choice_index].id}. New total:', self.candidates[next_choice_index].total)

                        else:
                          #  print(f'  Can\'t apply losing vote {self.candidates[next_choice_index].id} as this candidate has already lost.')
                            pass

                    else:
                        #print(f'   Voter {i} did not vote for {place_str(choice, "p")}.')
                        pass
                else:
                    #print(f'  Warning: Next choice {next_choice} is out of range. Do nothing.')
                    pass
