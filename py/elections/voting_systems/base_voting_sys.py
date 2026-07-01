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
from src.constants import FIRST_CHOICE, I_RIBBON, MAX_CHOICES, VOTE_BLANK 
from src.utils import name_len, show_banner

class BaseVotingSystem(ABC):

    """
    Base class for voting systems.

    Attributes:
        title (str): The title of the voting system.
        candidates (list): A list of candidates in the election.
        voters (list): A list of voters that cast ballots in the election.
        @todo - remove this line! winner_uid (int): The ID of the winning candidate.
        majority (int): The majority vote needed to win the election.
        voter_cnt (int): The number of voters in the election.
        choice_vals (list): Weighted choice values for each place.
    """

    def __init__(self, candidates: dict, voters: dict):
        self.candidates = candidates # Treat as a candidate pool
        self.voters = voters
        self._pool = CandidatePool(candidates)
        self.majority = self._get_majority_cnt()
        self.max_choice = self._get_max_choice()
        self.title = " System Results"
        self.winner = None
        self._name_len = name_len(self.candidates.values())
        

    def _get_majority_cnt(self) -> int:
        return (len(self.voters) // 2) + 1

    def _clear_totals(self, candidates: dict | list) -> dict | list:
        for candidate in candidates.values():
            candidate.total = 0

        return candidates


    def tally_totals(self, choice: int=FIRST_CHOICE, use_pool: bool=True, clear_totals: bool=False) -> None:
        # Fetch the data source
        candidates = self._pool.get() if use_pool else self.candidates
        
        if clear_totals:
            candidates = self._clear_totals(candidates)
            
        # Tally votes using the instant dictionary lookup
        for _, voter in self.voters.items():
            # Skip the voter if they didn't rank candidates this far.
            if choice >= len(voter.ballot):
                logging.debug(f"Voter {voter.uid} has an exhausted ballot for choice index {choice}. Skipping...")
                continue
                
            ballot_choice = voter.ballot[choice]
            
            # FIX B: Handle VOTE_BLANK explicitly so blank entries don't throw warnings
            if ballot_choice == VOTE_BLANK:
                continue
                
            if ballot_choice in candidates:
                candidates[ballot_choice].total += 1
            else:
                logging.warning(f"Skipping vote: Candidate UID '{ballot_choice}' not found.")
                
        # Save results back instantly
        if use_pool:
            # Pass a clean dictionary copy back to prevent turning self._data into a dict_values view wrapper
            self._pool.update_all(dict(candidates))
        else:
            self.candidates = dict(candidates)
 

    def tally_totals_orig(self, choice: int=FIRST_CHOICE, use_pool: bool=True, clear_totals: bool=False) -> None:

        # Fetch the data source
        candidates = self._pool.get() if use_pool else self.candidates
      
        if clear_totals:
            candidates = self._clear_totals(candidates)
 
        # Tally votes using the instant dictionary lookup
        for _, voter in self.voters.items():
            ballot_choice = voter.ballot[choice]
           
            if ballot_choice in candidates:
                candidates[ballot_choice].total += 1
            else:
                logging.warning(f"Skipping vote: Candidate UID '{ballot_choice}' not found.")
                
        # Save results back instantly
        if use_pool:
            self._pool.update_all(candidates)
        else:
            self.candidates = candidates
            
    def show_results(self) -> None:
        if self.winner:
           
            subtitles = []
            for candidate in self._pool.all().values():
                padding_len = self._name_len["max"] - len(candidate.name)
                padding = (" " * padding_len)
             
                # The ultra-clean, production-ready 1-liner alternative:
                line = f"Candidate: {candidate.name:<{self._name_len['max']}} | Total: {candidate.total}"

                subtitles.append(line)

            show_banner(self.title, subtitles)
            msg = f"\n{I_RIBBON} Winner: {self.winner.name} ({self.winner.party}) Total: {self.winner.total}\n"
            print(msg)
            logging.info(msg)
        
        else:
            logging.warning("No winner!")
            show_banner(self.title, "No winner!")

    def _get_max_choice(self) -> int:
        return min(MAX_CHOICES, len(self.candidates))

    def determine_winner(self, candidate: Candidate) -> bool:
        logging.debug(f"determine_winner(): if candidate:{candidate.uid} {candidate.total} >= {self.majority}:")
        if candidate.total >= self.majority or self._pool.length == 1:
            candidate.is_winner = True
            self.winner = candidate
            self._pool.update(candidate)
            return True
        
        return False 

    @abstractmethod
    def results():
        pass

    def determine_loser(self, choice: int = FIRST_CHOICE) -> Candidate | None:
        loser_pool = self._pool.get()

        logging.debug(f"loser_pool initial size: {len(loser_pool)}")
        logging.debug(loser_pool)
   
        # Continue looking for a single loser as long as there is a tie
        # and we haven't run out of voter choice preferences
        while len(loser_pool) > 1 and choice < self.max_choice:
            lowest = []
            lowest_total = float('inf')  # Reset threshold to infinity each round
            
            logging.debug(f"Evaluating tie-breaker at choice index: {choice}")

            # Extract just the raw candidate objects regardless of input type.
            if isinstance(loser_pool, dict):
                candidates_to_check = loser_pool.values()
            elif hasattr(loser_pool, 'items'): # Catch dict_items or similar structures safely
                candidates_to_check = [c for _, c in loser_pool.items()]
            else:
                candidates_to_check = loser_pool # Already a list of objects
                
            for candidate in candidates_to_check:
                current_votes = candidate.votes[choice]
                if current_votes < lowest_total:
                    lowest_total = current_votes
                    lowest = [candidate]
                    logging.debug(f"New lowest candidate found: {candidate.uid} with {lowest_total} votes")
                    
                elif current_votes == lowest_total:
                    lowest.append(candidate)
                    logging.debug(f"Appending lowest tied candidate: {candidate.uid}")
            
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
