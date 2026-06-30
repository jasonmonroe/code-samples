# voting_systems/weighted_sys.py

"""
+----------------------------------------------------------------------------
| WEIGHTED VOTING SYSTEM
+----------------------------------------------------------------------------
| Score all voting systems and then assign weight to each one of them.  Then
| determine the placement of candidates by utilizing all systems.
|
+----------------------------------------------------------------------------
"""

from voting_systems.base_voting_sys import BaseVotingSystem


class WeightedSystem(BaseVotingSystem):
    def __init__(self, candidates: dict, voters: dict):
        super().__init__(candidates, voters) 
        
        self.title = "Weighted Voting" + self.title

    def results():
        pass