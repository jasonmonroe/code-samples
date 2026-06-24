# voting_systems/ranked_choice_sys.py

"""
+----------------------------------------------------------------------------
| RANK CHOICE VOTING SYSTEM
+----------------------------------------------------------------------------
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

from voting_systems.base_voting_sys import BaseVotingSystem


class RankChoiceVotingSystem(BaseVotingSystem):
    def __init__(self, candidates: list, ballots: list):
        super().__init__(candidates, ballots) 
        
        self.title = "Rank Choice Voting" + self.title
        