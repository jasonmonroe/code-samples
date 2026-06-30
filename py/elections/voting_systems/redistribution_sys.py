# voting_systems/redistribution.py

"""
+----------------------------------------------------------------------------
| REDISTRIBUTION VOTING SYSTEM
+----------------------------------------------------------------------------
| Redistribute votes by eliminating worst performing candidate.  Then taking
| every voter who voted {place} and get their {next place} vote and apply
| it to the candidate.
| Repeat it until someone has a majority (totals) or whomever has the most 
| votes at the end of all rounds.
+----------------------------------------------------------------------------
"""

# Python Libraries
import logging

# Local Libraries
from src.constants import FIRST_CHOICE, MAX_CHOICES
from voting_systems.base_voting_sys import BaseVotingSystem


class RedistributionSystem(BaseVotingSystem):
    def __init__(self, candidates: dict, voters: dict):
        super().__init__(candidates, voters) 
        
        self.ballot_index = {}
        self.title = "Redistribution Voting" + self.title

    def results(self):
        choice = FIRST_CHOICE

        self._pool.reset()
        
        while choice < self.max_choice:
            # Only tally the totals in the first round, after that we will tally when we redistribute.
            if choice == FIRST_CHOICE:
                self.tally_totals()

            for _, candidate in self._pool.get().items():
                if self.determine_winner(candidate):
                    break

            if self.winner is not None:
                logging.info("Winner found!")
                break

            logging.debug(f"checking for loser on choice = {choice}")
            loser_candidate = self.determine_loser(choice)
            if loser_candidate is not None:
                self._redistribute_votes(loser_candidate.uid, choice)
                logging.warning(f"This version we will not remove {loser_candidate.uid} from the pool.  Just count the votes.")
                self._pool.remove(loser_candidate)
                
            else:
                logging.error("No losing candidate found.")
                
            choice += 1
        
        self._pool.show()


    def _redistribute_votes_orig(self, loser: str, choice: int) -> None:
        logging.debug(f"_redistribute_votes({loser, choice})")
        next_choice = choice + 1

        for _, voter in self.voters.items():
            logging.debug(f"if voter:{voter.uid} choice[{choice}] {voter.ballot[choice]} == {loser}:")
            if voter.ballot[choice] == loser:
                next_choice_uid = voter.ballot[next_choice]
                logging.debug(f"voter:{voter.uid} next choice vote is {next_choice_uid}.")

                # Apply the next choice vote to the remaining candidate.
                self._pool.update_by_uid(next_choice_uid, "total", 1)

    def _redistribute_votes(self, loser: str, choice: int) -> None:
        logging.debug(f"Redistributing votes for eliminated candidate: {loser}")
        next_choice = choice + 1
        
        # 1. Instantly grab ONLY the voters who chose the loser this round.
        # If you have 174M voters, but only 5,000 voted for the loser, 
        # this loop runs exactly 5,000 times instead of 174,000,000 times!
        loser_voters = self.ballot_index.pop(loser, [])
        
        for voter in loser_voters:
            next_choice_uid = voter.ballot[next_choice]
            logging.debug(f"voter:{voter.uid} next choice vote is {next_choice_uid}.")
            
            # Apply the vote change in memory
            self._pool.update_by_uid(next_choice_uid, "total", 1)
            
            # Move this voter into their next choice's active bucket for subsequent rounds
            if next_choice_uid in self.ballot_index:
                self.ballot_index[next_choice_uid].append(voter)

    def _build_ballot_index(self, choice: int):
        self.ballot_index = {}
        for voter in self.voters.values():
            ballot_choice = voter.ballot[choice]
            if ballot_choice not in self.ballot_index:
                self.ballot_index[ballot_choice] = []
            self.ballot_index[ballot_choice].append(voter)
            
        # THE CRITICAL FIX: Explicitly return the dictionary!
        return self.ballot_index

     