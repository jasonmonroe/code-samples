# voting_systems/popular_sys.py

"""
+----------------------------------------------------------------------------
| POPULAR VOTING SYSTEM
+----------------------------------------------------------------------------
| This systerm counts only the first place votes and picks the winner by whom 
| has the highest tally. No majority needed. Only one around.  
|
| Note: If there's a tie, remove the least voted candidate, reset the total 
| and count {next place} votes to pick winner. 
|
| Note: If there's a tile, just count the next place votes to pick winner.
| If by a small chance all the votes are the same then display no winner.
|
+----------------------------------------------------------------------------
"""

# Python Libraries
import logging

# Local Libraries
from src.constants import FIRST_CHOICE
from src.utils import placement
from voting_systems.base_voting_sys import BaseVotingSystem


class PopularVotingSystem(BaseVotingSystem):
    def __init__(self, candidates: dict, voters: dict):
        super().__init__(candidates, voters) 
        
        self.title = "Popular Vote" + self.title

    def results(self) -> None:
        self._pool.reset()
        candidates = self._pool.get()
        choice = FIRST_CHOICE
        self.tally_totals()
        
        while choice < self.max_choice:
            highest_total = 0
            highest = []
            
            # Instantly extract just the candidate objects regardless of input type
            if isinstance(candidates, dict):
                cand_objects = candidates.values()
            else:
                cand_objects = candidates  # Already a list of objects
                
            # Loop through the objects directly (Bypasses .items() completely)
            for candidate in cand_objects:
                if candidate.votes[choice] > highest_total:
                    highest_total = candidate.votes[choice]
                    highest = [candidate]
                elif candidate.votes[choice] == highest_total:
                    highest.append(candidate)
                    
            # Has anyone won yet?
            if self.determine_winner(highest, choice):
                break
            else:
                # If no winner, narrow the candidate pool to only the tied leaders
                candidates = highest
                
            # Go to next choice
            choice += 1

    # Override parent class
    def determine_winner(self, candidates: list, choice: int) -> bool |  None:
        if len(candidates) == 0: # This will never hit!
            logging.error("There is no one in the lead after the first round.  Check data.")
            return None
            
        elif len(candidates) == 1:
            # Winner has been determined (set) so end the loop
            logging.info("Success! We have a winner!")

            candidates[0].is_winner = True
            self.winner = candidates[0]

            self.candidates = candidates
            self._pool.update_all(self.candidates)
 
            return True
        else:
            # We have multiple leaders so lets go to second round.  Update the candidates by the "pool of winners."
            logging.info(f"No winner after {placement(choice, 'a')} round.  Limiting pool to {len(candidates)}.")
            return False
