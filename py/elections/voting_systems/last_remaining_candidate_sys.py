# voting_systems/last_remaining_candidate_sys.py

"""
+----------------------------------------------------------------------------
| LAST REMAINING CANDIDATE VOTING SYSTEM
+----------------------------------------------------------------------------
| No remaining candidates.  Count {first} place, if no majority, remove least
| voted candidate.  Repeat each place until one candidate is left.
| When counting a vote increment it to the total. The new majority will be 
| one vote over half of rounds * ballots.
|
+----------------------------------------------------------------------------
"""

from voting_systems.base_voting_sys import BaseVotingSystem


class LastRemainingCandidateSystem(BaseVotingSystem):
    def __init__(self, candidates: list, ballots: list):
        super().__init__(candidates, ballots) 
        
        self.title = f"Weighted Voting" + self.title


    def results() -> None:
        pass

    def determine_winner():
        pass

    def determine_loser():
        pass