# voting_systems/base_voting_sys.py
"""
+----------------------------------------------------------------------------
| BASE VOTING SYSTEM
+----------------------------------------------------------------------------
| Parent abstract class for all voting systems.  
|
+----------------------------------------------------------------------------
"""

# Python Libraries
import logging
from abc import ABC, abstractmethod

# Local Libraries
from src.constants import FIRST_CHOICE, I_RIBBON
from src.utils import get_index_by_uid, show_banner

class BaseVotingSystem(ABC):

    """
    Base class for voting systems.

    Attributes:
        title (str): The title of the voting system.
        candidates (list): A list of candidates in the election.
        voters (list): A list of voters that cast ballots in the election.
        winner_uid (int): The ID of the winning candidate.
        majority (int): The majority vote needed to win the election.
        voter_cnt (int): The number of voters in the election.
        choice_vals (list): Weighted choice values for each place.
    """

    def __init__(self, candidates: list, voters: list):
        self.candidates = candidates # Treat as a candidate pool
        self.candidate_pool = candidates.copy()
        self.voters = voters
        #self.voter_cnt = len(self.voters)
        self.title = " System Results"
        self.winner_uid = None
        self.winner = None
        self.majority = self._get_majority_cnt()


    def _get_majority_cnt(self) -> int:
        return (len(self.voters) // 2) + 1

    def _clear_totals(self, candidates: list) -> list:
        for candidate in candidates:
                candidate.total = 0
                
        return candidates

    def _sync_pool(self):
        self.candidate_pool = self.candidates

    def tally_totals(self, 
        choice: int=FIRST_CHOICE, # Which round are we voting on.  Default = 0
        clear_totals: bool=False, # Whether we set total = 0
        use_pool: bool=True       # Use candidate_pool instead of candidates
        ) -> None:

        attrs = {
            'choice': choice,
            'clear_totals': clear_totals,
            'use_pool': use_pool,
        }
        logging.debug(f"DBG: tally_totals() - {attrs}")
        
        # Get candidates
        candidates = self.candidate_pool if use_pool else self.candidates
        logging.debug(f"candidates={candidates}")
        if clear_totals:
            candidates = self._clear_totals(candidates)
        
        for voter in self.voters:
            logging.debug(f"voter={voter.__dict__}")
            for voter_candidate_uid in voter.ballot:
                #voter_candidate_uid = ballot_choice
                logging.debug(f"voter_candidate_uid={voter_candidate_uid}")
                idx = get_index_by_uid(candidates, voter_candidate_uid)
                candidates[idx].total += 1

        if not clear_totals and not use_pool:
            self.candidates = candidates
            self._sync_pool()
        elif use_pool:
            self.candidate_pool = candidates
        else:
            self.candidates = candidates

    def show_results(self) -> None:
        if self.winner:
            subtitles = []
            for candidate in self.candidates:
                line = f"Candidate: {candidate.name} | Total: {candidate.total}"
                subtitles.append(line)

            show_banner(self.title, subtitles)
            msg = f"\nWinner: {I_RIBBON} {self.winner.name} ({self.winner.party})\n"
            print(msg)
            logging.info(msg)
        
        else:
            logging.warning("No winner!")
            show_banner(self.title, "No winner!")
            
        self.candidate_pool = []

    @abstractmethod
    def results():
        pass
    
    @abstractmethod
    def determine_winner():
        pass

    @abstractmethod
    def determine_loser():
        pass
