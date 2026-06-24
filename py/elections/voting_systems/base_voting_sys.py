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
from src.candidate import Candidate
#from src.candidate_pool import CandidatePool
from src.constants import FIRST_CHOICE
from src.utils import get_index_by_uid

class BaseVotingSystem(ABC):

    """
    Base class for voting systems.

    Attributes:
        title (str): The title of the voting system.
        candidates (list): A list of candidates in the election.
        ballots (list): A list of ballots cast in the election.
        winner_id (int): The ID of the winning candidate.
        majority (int): The majority vote needed to win the election.
        voter_cnt (int): The number of voters in the election.
        choice_vals (list): Weighted choice values for each place.
    """

    def __init__(self, candidates: list, ballots: list):
        #self.all_candidates = candidates.copy() # Treat as original
        self.candidates = candidates # Treat as a candidate pool
        self.candidate_pool = candidates.copy()
        self.pool = [] # @todo - delete
        #self.candidate_pool = []
        #self.candidate_pool = CandidatePool(self.candidates)
        #self.pool = self.candidate_pool.clear()
        self.ballots = ballots
        self.ballot_cnt = len(self.ballots)
        self.title = " System Results"
        #self.candidate_pool = []
        self.winner_uid = None
        self.winner = None
        self.majority = self._get_majority_cnt()
        self.choice_vals = []
        self.vote_cnts = []
        self.round = 0

    def _get_majority_cnt(self) -> int:
        half = round(self.ballot_cnt / 2)

        if self.ballot_cnt % 2 == 0:
            return half + 1

        return half

    #@todo - delete
    def _get_candidate_pool(self) -> list:
        #pool = CandidatePool(self.candidate_pool)
        #pool.reset()
        #return pool.pool()
        return []
    #@todo - delete
    def clear_candidate_pool(self) -> None:
        self.candidate_pool = []

    #@todo - delete
    def reset_candidate_pool(self) -> None:
        logging.info('Resetting candidate pool.')
        print("Resetting candidate pool...")
        #pool = []
        #for _ in range(len(self.candidates)):
        #    pool.append(self.candidates)
        # Update candidate pool with a copy of candidates.
        self.candidate_pool = []
        self.candidate_pool = self.candidates.copy()

    #@todo - delete
    def add_to_candidate_pool(self, candidate: Candidate):
        self.candidate_pool.append(candidate)

    #@todo - delete
    def remove_loser(self, candidate):
        self.candidate_pool.remove(candidate)

    #def remove_from_candidate_pool(self, candidate: Candidate):
    #    self.candidate_pool.pop(candidate)

    def _clear_totals(self, use_pool: bool=True) -> None:
        if use_pool:
            for candidate in self.candidate_pool:
                candidate.total = 0
        else:
            for candidate in self.candidates:
                candidate.total = 0

    def _sync_pool(self):
        self.candidate_pool = self.candidates

    def calc_totals(self, 
        choice: int=FIRST_CHOICE, # Which round are we voting on.  Default = 0
        clear_totals: bool=False, # Whether we set total = 0
        use_pool: bool=True # Use candidate_pool instead of candidates
        ) -> None:

        # Get candidates
        candidates = self.candidate_pool if use_pool else self.candidates
        
        if clear_totals:
            self._clear_totals(candidates, use_pool)
        
        for ballot in self.ballots:
            idx = get_index_by_uid(candidates, ballot[choice])
            candidates[idx].total += 1

        # Update both if initializing.  This is so  the candidates and candidate pools have the updated totals
        if not clear_totals and not use_pool:
            print("DBG: Assuming its on intialization. Updating candidates and pool.")
            self.candidates = candidates
            self._sync_pool()
        else:

            if use_pool:
                self.candidate_pool = candidates
            else:
                self.candidates = candidates

        


    @abstractmethod
    def determine_loser():
        pass

    @abstractmethod
    def determine_winner():
        pass

    @abstractmethod
    def check_tie():
        pass
    
    @abstractmethod
    def break_tie():
        pass

    @abstractmethod
    def show_results():
        pass
