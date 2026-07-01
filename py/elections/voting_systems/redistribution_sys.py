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
from src.constants import FIRST_CHOICE
from voting_systems.base_voting_sys import BaseVotingSystem


class RedistributionSystem(BaseVotingSystem):
    def __init__(self, candidates: dict, voters: dict):
        super().__init__(candidates, voters) 
        
        self.ballot_index = {}
        self.title = "Redistribution Voting" + self.title

    def results(self) -> None:
        choice = FIRST_CHOICE

        self._pool.reset()
        self._build_ballot_index(choice=FIRST_CHOICE)
        
        while choice < self.max_choice:
            # Only tally the totals in the first round, after that we will tally when we redistribute.
            if choice == FIRST_CHOICE:
                self.tally_totals()
                logging.debug("\n")

            for _, candidate in self._pool.get().items():
                if self.determine_winner(candidate):
                    break

            if self.winner:
                logging.info("Winner found!")
                break

            loser_candidate = self.determine_loser(choice)

            if loser_candidate:
                self._redistribute_votes(loser_candidate.uid, choice)
                self._pool.remove(loser_candidate)
                
            else:
                logging.error("No losing candidate found.")
                
            choice += 1
        
        self._pool.show()

    def _redistribute_votes_orig(self, loser: str, choice: int) -> None:
        logging.debug(f"_redistribute_votes_orig({loser, choice})")
        
        for _, voter in self.voters.items():
            logging.debug(f"if voter:{voter.uid} choice[{choice}] {voter.ballot[choice]} == {loser}:")
            if voter.ballot[choice] == loser:
                
                next_choice_uid = None
                next_choice = choice + 1
                while next_choice < len(voter.ballot):
                    logging.debug(f"Does loser {loser} exist in pool?")
                    if self._pool.exists(loser):
                        next_choice_uid = voter.ballot[next_choice]
                        break
                    else:
                        logging.debug(f"No! loser does not exist, go to next choice {next_choice+1}")
                        next_choice + 1
                
                logging.debug(f"voter:{voter.uid} next choice vote is {next_choice_uid}.")
                
                # Apply the next choice vote to the remaining candidate.
                if next_choice_uid:
                    self._pool.update_by_uid(next_choice_uid, "total", 1)

    def _redistribute_votes(self, loser: str, choice: int) -> None:
        logging.debug(f"Redistributing votes for eliminated candidate: {loser}")
        
        # Instantly grab ONLY the voters who chose the loser this round.
        loser_voters = self.ballot_index.pop(loser, [])
        logging.debug(f"loser_voters count: {len(loser_voters)}")
        
        for voter in loser_voters:
            logging.debug(f"losing voter={voter.uid}")
            
            # Start scanning preferences right after the current round's choice position
            next_choice = choice + 1
            allocated = False
            
            # Loop through subsequent ballot ranks until an ACTIVE candidate is found
            while next_choice < len(voter.ballot):
                next_choice_uid = voter.ballot[next_choice]
                
                # Check if this next candidate exists and is active in your pool
                if self._pool.exists(next_choice_uid):
                    logging.debug(f"_redistribute_votes(): voter:{voter.uid} next valid choice vote is {next_choice_uid}.")
                    
                    # Apply the vote change in memory
                    self._pool.update_by_uid(next_choice_uid, "total", 1)
                    
                    # Move this voter into their next choice's active bucket for subsequent rounds
                    if next_choice_uid in self.ballot_index:
                        self.ballot_index[next_choice_uid].append(voter)
                    else:
                        # Fallback initialization in case the bucket wasn't instantiated
                        self.ballot_index[next_choice_uid] = [voter]
                        
                    allocated = True
                    logging.debug("BREAK!")
                    break  # Vote successfully transferred! Stop scanning this voter's ballot.
                
                # If next_choice_uid is already eliminated, log it and keep scanning forward
                logging.debug(f"voter:{voter.uid} choice at rank {next_choice} ({next_choice_uid}) is eliminated. Skipping...")
                next_choice += 1
                
            # Handle exhausted ballots gracefully if no active choices remain
            if not allocated:
                logging.info(f"voter:{voter.uid} has an exhausted ballot (no active candidates remaining).")

        logging.debug(f"Redistributing votes for eliminated candidate: {loser}")
        next_choice = choice + 1
        
        # 1. Instantly grab ONLY the voters who chose the loser this round.
        # If you have 174M voters, but only 5,000 voted for the loser, 
        # this loop runs exactly 5,000 times instead of 174,000,000 times!
        loser_voters = self.ballot_index.pop(loser, [])
        
        for voter in loser_voters:
            logging.debug(f"losing voter={voter}")
            next_choice_uid = voter.ballot[next_choice]
            logging.debug(f"_redistribute_votes(): voter:{voter.uid} next choice vote is {next_choice_uid}.")
            
            # Apply the vote change in memory
            self._pool.update_by_uid(next_choice_uid, "total", 1)
            
            # Move this voter into their next choice's active bucket for subsequent rounds
            if next_choice_uid in self.ballot_index:
                self.ballot_index[next_choice_uid].append(voter)

    def _build_ballot_index(self, choice: int) -> dict:
        self.ballot_index = {}
        for voter in self.voters.values():
            ballot_choice = voter.ballot[choice]
            if ballot_choice not in self.ballot_index:
                self.ballot_index[ballot_choice] = []
            self.ballot_index[ballot_choice].append(voter)
            
        return self.ballot_index
