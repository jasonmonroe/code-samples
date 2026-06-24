# voting_systems/base_voting_sys.py

"""
+----------------------------------------------------------------------------
| Base Voting System
+----------------------------------------------------------------------------
| Parent abstract class for all voting systems.  
|
"""

# Python Libraries
import logging
from abc import ABC, abstractmethod

# Local Libraries
from src.candidate import Candidate

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
        self.candidates = candidates
        self.ballots = ballots
        self.ballot_cnt = len(self.ballots)
        self.title = ''
        self.candidate_pool = []
        self.winner_uid = None
        self.majority = self._get_majority_cnt()
        self.choice_vals = []
        self.vote_cnts = []

    def _get_majority_cnt(self) -> int:
        half = round(self.ballot_cnt / 2)

        if self.ballot_cnt % 2 == 0:
            return half + 1

        return half

    def clear_candidate_pool(self) -> None:
        self.candidate_pool = []

    def reset_candidate_pool(self) -> None:
        logging.info('Resetting candidate pool.')
        print("Resetting candidate pool...")
        #pool = []
        #for _ in range(len(self.candidates)):
        #    pool.append(self.candidates)
        # Update candidate pool with a copy of candidates.
        self.candidate_pool = []
        self.candidate_pool = self.candidates.copy()

    def add_to_candidate_pool(self, candidate: Candidate):
        self.candidate_pool.append(candidate)

    def remove_loser(self, candidate):
        self.candidate_pool.remove(candidate)

    #def remove_from_candidate_pool(self, candidate: Candidate):
    #    self.candidate_pool.pop(candidate)

         
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
    def score_ballots():
        pass

    @abstractmethod
    def show_results():
        pass
