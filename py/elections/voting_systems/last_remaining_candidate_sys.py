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

import logging
from src.candidate import Candidate
from src.constants import FIRST_CHOICE
from voting_systems.base_voting_sys import BaseVotingSystem


class LastRemainingCandidateSystem(BaseVotingSystem):
    def __init__(self, candidates: dict, voters: dict):
        super().__init__(candidates, voters) 
        
        self.title = f"Last Remaining Voting" + self.title

    def results(self) -> None:
        self._remove_blank_votes()
        choice = FIRST_CHOICE
        self._pool.reset()
        
        while choice < self.max_choice:
            # Get a fresh active pool snapshot at the start of each round loop
            candidates = self._pool.get()
            
            # Tally the pure totals based on the current choice index layer
            self.tally_totals(choice=choice)
            logging.debug("\n")
            
            # Loop over a static list of keys to prevent KeyErrors from deletions
            for uid in list(candidates):
                candidate = candidates[uid]
                
                # Check your custom single-survivor rule instead of base majority rules
                if self.determine_winner(candidate):
                    break
                    
            # Break the while loop if an internal check found the absolute winner
            if self.winner:
                logging.info("Winner found!")
                break
                
            # Find and remove the lowest candidate for this round layer
            loser_candidate = self.determine_loser(choice)
            if loser_candidate:
                # Safely eliminates the loser before the next round begins (No redistribution)
                self._pool.remove(loser_candidate)
                
            choice += 1

    def determine_winner(self, candidate: Candidate) -> bool:
        """Declares victory only when a single survivor remains in the candidate pool."""
        if self._pool.length == 1:
            candidate.is_winner = True
            self.winner = candidate
            self._pool.update(candidate)
            
            return True

        return False
