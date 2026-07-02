# src/voter.py

# Python Libraries
from datetime import datetime, timedelta
import logging
import random

# Local Libraries
from src.candidate_chooser import CandidateChooser
from src.constants import BALLOT_BLANK, FIRST_CHOICE, MAX_CHOICES, PERCENTILE, VOTE_BLANK_PCT_THRESH
from src.utils import gen_uuid, placement


class Voter:
    def __init__(self, earliest_at: str, add_noise: bool=False) -> None:
        self.add_noise = add_noise
        self.uid = gen_uuid(6)
        self.ballot = BALLOT_BLANK[:]  
        self.registered_at = self._log_registered_at(earliest_at)
        self.voted_at = None
        logging.debug(f"Voter: {self.uid} registered_at: {self.registered_at}")
        
    def _log_registered_at(self, earliest_at: str) -> str:
        # A voter can register on the date of the election or at the earliest registion date.
        # Parse the earliest registration string into an object
        earliest_date_obj = datetime.strptime(earliest_at, "%B %d, %Y")
        
        # Get today's date (election day context)
        today = datetime.now()
        
        # Calculate the actual window duration in days (Today - Earliest Date)
        # This yields a correct range (e.g., 365 days if earliest_at is June 26, 2025)
        delta = today - earliest_date_obj
        duration = max(0, delta.days) 
  
        # Pick a random day within that realistic window
        register_day = random.randint(0, duration)
        
        # Subtract the random offset from today to get a valid registration date
        return (today - timedelta(days=register_day)).strftime("%B %d, %Y %H:%M:%S")

    def execute(self, candidate_chooser: CandidateChooser, choice: int=FIRST_CHOICE) -> str | None:
        candidate_chosen = candidate_chooser.decision(choice)
        self.ballot[choice] = candidate_chosen
        
        if choice == MAX_CHOICES - 1:
            if not self._check_ballot_uniqueness():
                self.ballot[choice] = candidate_chooser.decision(choice)
        
        self.voted_at = datetime.now().strftime("%B %d, %Y %H:%M:%S")
        logging.info(f"✅ Voter {self.uid} voted for candidate {self.ballot[choice]} as {placement(choice)} choice at {self.voted_at}.")

        return candidate_chosen

    def voted(self) -> bool:
        # Will this registered voter even bother to vote?
        if self.add_noise:
            no_vote_odds = random.randint(0, PERCENTILE)
            if no_vote_odds < VOTE_BLANK_PCT_THRESH:
                logging.warning(f"Voter {self.uid} did not cast a ballot.")
                self.voted_at = None
                return False

        return True

    def _check_ballot_uniqueness(self) -> bool:
        unique_ballot = list(dict.fromkeys(self.ballot))
        if self.ballot != unique_ballot:
            logging.error(f"Voter {self.uid} ballot not unique: {self.ballot}")
            return False
        
        return True
        