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
from src.candidate_pool import CandidatePool
from src.constants import FIRST_CHOICE, I_RIBBON, MAX_CHOICES, VOTE_BLANK
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
        self._pool = CandidatePool(candidates)
        self.voters = voters
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

    def tally_totals(self, 
        choice: int=FIRST_CHOICE, # Which round are we voting on.  Default = 0
        clear_totals: bool=False, # Whether we set total = 0
        use_pool: bool=True       # Use candidate_pool instead of candidates
        ) -> None:
        
        # Get candidates
        candidates = self._pool.get() if use_pool else self.candidates
         
        if clear_totals:
            candidates = self._clear_totals(candidates)
        
        for voter in self.voters:
            ballot_choice = voter.ballot[choice]
            idx = get_index_by_uid(candidates, ballot_choice)
            candidates[idx].total += 1

        if not clear_totals and not use_pool:
            self.candidates = candidates
            self._pool.reset()
            #self._sync_pool()
        elif use_pool:
            self._pool.update(candidates)
            #self.candidate_pool = candidates
            #self._pool.reset()
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
            
        self._pool.clear()

    def _get_max_choice(self) -> int:
        return min(MAX_CHOICES, len(self.candidates))

    def _sync_pool(self):
        self.candidate_pool = self.candidates

    @abstractmethod
    def results():
        pass
    
    @abstractmethod
    def determine_winner():
        pass

    @abstractmethod
    def determine_loser():
        pass
