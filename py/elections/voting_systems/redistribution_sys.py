# voting_systems/redistribution.py

"""
+----------------------------------------------------------------------------
| REDISTRIBUTION VOTING SYSTEM
+----------------------------------------------------------------------------
| Redistribute votes by eliminating worst performing candidate.  Then taking
| every voter who voted {place} and get their {next place} vote and apply
| it to the candidate.
| Repeat it until someone has a majority (totals) or whomever has the most votes at
| the end of all rounds.
|
+----------------------------------------------------------------------------
"""

# Python Libraries
import logging

# Local Libraries
from src.constants import FIRST_CHOICE, MAX_CHOICES
from voting_systems.base_voting_sys import BaseVotingSystem


class RedistributionSystem(BaseVotingSystem):
    def __init__(self, candidates: list, ballots: list):
        super().__init__(candidates, ballots) 
        
        self.title = "Redistribution Voting" + self.title

    def results(self):
        choice = FIRST_CHOICE
        max_choice = self._get_max_choice()
         
        while choice < max_choice:
            # Only tally the totals in the first round, after that we will tally when we redistribute.
            if choice == FIRST_CHOICE:
                self.tally_totals(choice)

            for candidate in self._pool.get():
                logging.debug(f"choice = {choice}")
                if self.determine_winner(candidate):
                    break

            if self.winner:
                logging.info("Winner found!")
                break

            logging.debug(f"checking for loser on choice = {choice}")
            loser_candidate = self.determine_loser(choice)
            if loser_candidate is None:
                logging.error("No losing candidate found.")

            else:
                # Take their
                self.redistribute_votes(loser_candidate.uid, choice)
                self._pool.remove(loser_candidate)

            choice += 1

    def redistribute_votes(self, loser: str, choice: int) -> None:
        logging.debug(f"redistribute_votes({loser, choice})")
        next_choice = choice + 1

        if next_choice == MAX_CHOICES:
            logging.warning("There is no next choice! Return None")
            return None

        logging.debug(f"Voters: {len(self.voters)}")

        for voter in self.voters:
            logging.debug(f"if voter:{voter.uid} choice[{choice}] {voter.ballot[choice]} == {loser}:")
            if voter.ballot[choice] == loser:
                next_choice_uid = voter.ballot[next_choice]
                logging.debug(f"voter:{voter.uid} next choice vote is {next_choice_uid}.")

                # Apply the next choice vote to the remaining candidate.
                self._pool.update_by_uid(next_choice_uid, "total", 1)
        