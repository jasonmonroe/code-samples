# voting_systems/redistribution.py

"""
+----------------------------------------------------------------------------
| REDISTRIBUTION VOTING SYSTEM
+----------------------------------------------------------------------------
| Redistribute votes by eliminating worst performing candidate.  Then taking
| the every voter who voted {place} and get their {next place} vote and apply
| it to the candidate.
| Repeat it until someone has a majority or whomever has the most votes at
| the end of all rounds.
|
+----------------------------------------------------------------------------
"""

from voting_systems.base_voting_sys import BaseVotingSystem


class RedistributionSystem(BaseVotingSystem):
    def __init__(self, candidates: list, ballots: list):
        super().__init__(candidates, ballots) 
        
        self.title = "Redistribution Voting " + self.title