# voting_systems/ranked_choice_sys.py
"""
+----------------------------------------------------------------------------
| RANK CHOICE VOTING SYSTEM
+----------------------------------------------------------------------------
| This system is used by the state of Alaska. Instead of choosing one 
| candidate, you fill in the oval in column one for the candidate you would 
| most like to win, then vote for your second choice in column two and so on.  
| Ranking other candidates does not impact your first choice, and you do not 
| have to rank them all.  You should only mark one oval in each row and one 
| oval in each column.
|
| The ballots are tallied and scored by its first choice votes.  If a candidate
| gets at least half of the votes in round one, they win.  If this doesn't 
| happen, it's continued to next round and the candidate with the least nth 
| choice votes is eliminated.
|
| Count the voter's next remaining candidate choice instead of their choice 
| for the eliminated candidate (meaning they still have a say in whom wins).
|
| Repeat these steps in rounds until there are only two candidates and now 
| whomever has the most votes is determined the winner.
|
| Note: If a choice is blank shift it from the ballot.
|------
| @link https://www.elections.alaska.gov/election-information/
| @link https://www.youtube.com/watch?v=lLU3lbrxMBI
| @link https://www.youtube.com/watch?v=oHRPMJmzBBw
+----------------------------------------------------------------------------
"""

# Python Libraries
import logging

# Local Libraries
from src.constants import FIRST_CHOICE, I_CROSSMARK, VOTE_BLANK
from src.utils import placement
from voting_systems.base_voting_sys import BaseVotingSystem


class RankChoiceVotingSystem(BaseVotingSystem):
    def __init__(self, candidates: dict, voters: dict):
        super().__init__(candidates, voters) 
        self.title = "Rank Choice Voting" + self.title

    def results(self):
        logging.info(f"Majority needed to win: {self.majority}")
        
        self._remove_blank_votes()

        choice = FIRST_CHOICE
        max_itr = 0
        resets = 0
        while True and max_itr < 32:
            logging.debug(f"BEGIN -> choice:{choice}")
            logging.debug(f"=== Start {placement(choice, "a")} round ===".title())
            
            # Important: Always count the first choice regardless of round
            # because the loser will have their names removed from the ballots!
            self.tally_totals(clear_totals=True) 

            # Any candidate have a majority?
            for _, candidate in self._pool.get().items():
                if self.determine_winner(candidate):
                    break
                
            if self.winner:
                logging.info(f"Winner found! Iterations: {max_itr}.")
                break

            # If no winner, remove lowest performing candidate
            logging.info(f"No winner in {placement(choice, 'a')} round. Resets:{resets}")

            # Remove lowest candidate
            loser_candidate = self.determine_loser()

            # Remove loser candidate pool and ballots
            if loser_candidate:
                self._pool.remove(loser_candidate)
                self._shift_ballots(loser_candidate.uid)     
                
            logging.debug(f"--- After {placement(choice, "a")} round | Resets: {resets} ---".title())
             
            for _, candidate in self._pool.get().items():
                logging.debug(f"candidate: {candidate.uid} | total votes: {candidate.total}")

            if choice < self.max_choice - 1:
                choice += 1
            else:
                logging.warning(f"No majority of ({self.majority}) yet, so lets reset: {resets} the choice:{choice} to 0 again.")
                choice = 0
                resets += 1
                
            max_itr += 1
            logging.debug(f"max_itr={max_itr}, resets: {resets}")
   
    def _shift_ballots(self, loser_uid: str) -> None:
        logging.info(f"Shifting loser candidate[{loser_uid}] from ballot.")

        for uid, voter in self.voters.items():
            if loser_uid in voter.ballot:
                logging.debug(f"{I_CROSSMARK} Removing candidate[{loser_uid}] from voter[{uid}] ballot{voter.ballot} via shift.")
                voter.ballot.remove(loser_uid)
                logging.debug(f"Revised Voter[{voter.uid}] ballot: {voter.ballot}.")
