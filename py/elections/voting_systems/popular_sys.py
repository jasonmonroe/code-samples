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
from src.constants import FIRST_CHOICE, I_RIBBON, MAX_CHOICES
from src.utils import get_index_by_uid, placement, show_banner
from voting_systems.base_voting_sys import BaseVotingSystem


class PopularVotingSystem(BaseVotingSystem):
    def __init__(self, candidates: list, ballots: list):
        super().__init__(candidates, ballots) 
        
        self.title = "Popular Vote" + self.title


    def results(self) -> None:
        self.tally_totals()

        candidates = self.candidate_pool
        choice = FIRST_CHOICE

        while choice < MAX_CHOICES:
            print(f"{placement(choice, 'a').title()} round.")
            highest_total = 0
            highest = []
            
            # Check which candidate has the highest vote
            for candidate in candidates:
                if candidate.votes[choice] > highest_total:
                    highest_total = candidate.votes[choice]
                    highest = [candidate]
                elif candidate.votes[choice] == highest_total:
                    highest.append(candidate)
                
            # Has anyone won yet?
            if self.determine_winner(highest):
                break
            else: # If no winner, return pool of highest candidates
                candidates = highest
            
            # Go to next choice
            choice += 1
            logging.debug(f"Updating round to {choice}.")
            

    def determine_winner(self, candidates: list, choice: int) -> bool |  None:
        if len(candidates) == 0: # This will never hit!
            logging.error("There is no one in the lead after the first round.  Check data.")
            return None
            
        elif len(candidates) == 1:
            # Winner has been determined (set) so end the loop
            logging.info("Success! We have a winner.")
            self.winner = candidates[0]
            winner_idx = get_index_by_uid(self.winner.uid)
            self.candidates[winner_idx].is_winner = True
            #self.candidate_pool = []
            return True
        else:
            # We have multiple leaders so lets go to second round.  Update the candidates by the "pool of winners."
            logging.info(f"No winner after {placement(choice, 'a')} round.  Limiting pool to {candidates}.")
            return False

    
   

    def determine_loser():
        pass

         

    # Note: This method works but want to make it cleaner
    def determine_winner_orig(self):
        candidates = self.candidate_pool
        choice = FIRST_CHOICE

        while choice < MAX_CHOICES:
            print(f"{placement(choice, 'a').title()} round.")
            highest_total = 0
            winners = []
            
            # Check which candidate has the highest vote
            for candidate in candidates:
                if candidate.votes[choice] > highest_total:
                    highest_total = candidate.votes[choice]
                    winners = [candidate]
                elif candidate.votes[choice] == highest_total:
                    winners.append(candidate)
                else:
                    # remove candidate
                    pass

            if len(winners) == 0:
                logging.error("There is no one in the lead after the first round.  Check data.")

            # Has anyone won?
            if len(winners) == 1:
                logging.info("Success! We have a winner.")
                self.winner = winners[0]
                break
            else:
                # We have multiple leaders so lets go to second round.  Update the candidates by the "pool of winners."
                logging.info(f"No winner after {placement(choice, 'a')} round.  Limiting pool to {winners}.")
                candidates = winners
                
            # Go to next choice
            choice += 1
            logging.debug(f"Updating round to {choice}.")
 
