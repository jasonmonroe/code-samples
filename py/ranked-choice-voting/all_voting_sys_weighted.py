"""
|--------------------------------------------------------------------------
| All Voting Weighted System
|--------------------------------------------------------------------------
| Take the number of points of each candidate for each voting system and weigh
| them to determine an overall winner.
|
| Voting System Weights:
| - Popular Score: 10%
| - Weighted (Point) Score: 25%
| - Remaining Candidates: 40%
| - Redistribution: 25%
"""

from helpers import PERCENTILE, FIRST_CHOICE_INDEX
from voting_sys import VotingSystem


class AllVotingWeightedSystem():
    def __init__(self, results):

        self.title = 'All Weighted System'
        self.results = results
        self.candidates = []

        # Voting System Weights
        self.popular_weight = 0.10
        self.weighted_score_weight = 0.25
        self.remaining_candidates_weight = 0.40
        self.redistribution_weight = 0.25

        vote_sys = VotingSystem([], [])
        vote_sys.title = self.title
        vote_sys.show_banner()

        print(
            'Weights: Popular:', self.popular_weight * PERCENTILE,
            'Weighted Score:', self.weighted_score_weight * PERCENTILE,
            'Remaining Candidates:', self.remaining_candidates_weight * PERCENTILE,
            'Redistribution:', self.redistribution_weight * PERCENTILE
        )

    def score_ballots(self):
        """
        Score the ballots for each candidate in each voting system.

        :return:
        """

        for result in self.results:
            for candidate in result['candidates']:

                if result['title'] == 'Popular':
                    candidate.sys_totals += candidate.total * self.popular_weight

                elif result['title'] == 'Weighted Score':
                    candidate.sys_totals += candidate.total * self.weighted_score_weight

                elif result['title'] == 'Remaining Candidates':
                    candidate.sys_totals += candidate.total * self.remaining_candidates_weight

                elif result['title'] == 'Redistribution':
                    candidate.sys_totals += candidate.total * self.redistribution_weight

                # Append the candidate to the list
                self.candidates.append(candidate)

    def show_totals_by_sys(self):

        for result in self.results:
            print('\nVoting System:', result['title'])

            for candidate in result['candidates']:
                print(' Candidate:', candidate.id, 'Total:', candidate.total)

        # Calculate the total points for each candidate based on the weighted system.
        self.score_ballots()

        # Last result for all systems weighted.
        print('\n(All) Voting System:', self.title)
        for candidate in self.candidates:
            print(' Candidate:', candidate.id, 'Total:', candidate.sys_totals)

    def determine_winner(self):
        """
        Determine the winner of the election.

        :return:
        """
        # Sort the candidates by the total number of votes they have. Winner will be at the top.
        self.candidates = sorted(self.candidates, key=lambda candidate: candidate.sys_totals, reverse=True)

        winner = self.candidates[FIRST_CHOICE_INDEX]

        vote_sys = VotingSystem([], [])
        vote_sys.declare_winner(winner.name)
