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
from src.candidate_pool import CandidatePool
from src.constants import FIRST_CHOICE, I_RIBBON, MAX_CHOICES 
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
        logging.debug(f"count:{self._pool.length}")
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

    def determine_winner(self, candidate: Candidate) -> bool:
        logging.debug(f"if candidate:{candidate.uid} {candidate.total} >= {self.majority}:")
        if candidate.total >= self.majority:
            self.winner = candidate
            return True
        
        return False 

    @abstractmethod
    def results():
        pass

    def determine_loser(self, choice: int = FIRST_CHOICE) -> Candidate | None:
        loser_pool = self._pool.get()
        max_choice = self._get_max_choice()
        
        logging.debug(f"loser_pool initial size: {len(loser_pool)}")
        
        # Continue looking for a single loser as long as there is a tie
        # and we haven't run out of voter choice preferences
        while len(loser_pool) > 1 and choice < max_choice:
            lowest = []
            lowest_total = float('inf')  # Reset threshold to infinity each round
            
            logging.debug(f"Evaluating tie-breaker at choice index: {choice}")
            
            for candidate in loser_pool:
                current_votes = candidate.votes[choice]
                
                if current_votes < lowest_total:
                    lowest_total = current_votes
                    lowest = [candidate]
                    logging.debug(f"New lowest candidate found: {candidate.uid} with {lowest_total} votes")
                    
                elif current_votes == lowest_total:
                    lowest.append(candidate)
                    logging.debug(f"Appending tied candidate: {candidate.uid}")
            
            # If the tie is broken and we have exactly one loser, return them immediately
            if len(lowest) == 1:
                return lowest[0]
                
            # If still tied, narrow the pool to only these tied candidates and increment choice
            if len(lowest) > 1:
                logging.info(f"Tie persisted: {len(lowest)} candidates tied at {lowest_total} votes for choice {choice}.")
                loser_pool = lowest
                choice += 1
                
        # Absolute dead-lock tie: even after checking all choices, multiple candidates remain tied
        if len(loser_pool) > 1:
            logging.warning(f"Absolute tie detected between remaining candidates: {[c.uid for c in loser_pool]}.")
            # Optional: return loser_pool[0] or handle external tie-breaking rules (like a coin flip)
            
        logging.warning("No losing candidate found.")
        return None