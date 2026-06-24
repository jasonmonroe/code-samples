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

import logging

from src.constants import FIRST_CHOICE, I_RIBBON, MAX_CHOICES
from src.utils import placement, show_banner
from voting_systems.base_voting_sys import BaseVotingSystem


class PopularVotingSystem(BaseVotingSystem):
    def __init__(self, candidates: list, ballots: list):
        super().__init__(candidates, ballots) 
        
        self.title = "Popular Vote" + self.title

    def determine_winner(self):
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
            
    def show_results(self):
        if self.winner:
            subtitles = []
            for candidate in self.candidates:
                line = f"Candidate: {candidate.name} | Total: {candidate.total}"
                subtitles.append(line)

            show_banner(self.title, subtitles)
            print(f"\nWinner: {I_RIBBON} {self.winner.name} ({self.winner.party})\n")
        
        else:
            logging.warning("No winner!")
            show_banner(self.title, "No winner!")
            
    def check_tie():
        pass
       
    def break_tie():
        pass

    def determine_loser():
        pass
