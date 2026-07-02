# src/candidate_pool.py

import logging
from typing import Any
from src.candidate import Candidate


class CandidatePool:
    def __init__(self, candidates: dict) -> None:
        """
        input:
        candidates: list of candidate objects

        output: None
        """
        # Keep an immutable original roster backup if needed, but use self._data as the single source of truth for active candidates.
        self.candidates = candidates.copy()
        self._data = candidates.copy()
        self._removed = {}

    def add(self, candidate: Candidate) -> None:
        """Add a candidate to the active pool."""
        if candidate not in self._data:
            self._data[candidate.uid] = candidate

    def clear(self) -> None:
        self._data = {}
        self._removed = {}

    def get(self) -> dict:
        """Return the live pool of active candidates remaining in the election."""
        return self._data 

    @property
    def length(self) -> int:
        return len(self._data)

    def remove(self, candidate: Candidate | str) -> None:
        """Permanently remove an eliminated candidate from the active pool."""

        target_candidate = None

        # candidate is a uid
        if isinstance(candidate, str):
            target_candidate = candidate
            self._removed[target_candidate] = self._data[target_candidate]
        else:
            # Candidate is an object
            target_candidate = candidate.uid
            self._removed[target_candidate] = candidate
    
        self._data.pop(target_candidate, None)

        logging.info(f"Candidate {target_candidate} removed from active pool.")

        self.show()

    def reset(self) -> list[Candidate]:
        """Restore the active pool back to the initial starting candidates."""
    
        self.clear()
        self._data = self.candidates.copy()
        
        return self._data

    def update(self, candidate: Candidate) -> dict:
        if isinstance(candidate, Candidate):
            self._data[candidate.uid] = candidate
            self.candidates[candidate.uid] = candidate

    def all(self) -> dict:
        return self.candidates.copy()

    def exists(self, uid: str) -> bool:
        return uid in self._data 

    def update_all(self, candidates: dict) -> None:
        if isinstance(candidates, dict):
            self._data = candidates
            #self.candidates = candidates

    def update_by_uid(self, uid: str, key: str, value: Any) -> bool:
        """Safely modify or increment an attribute of an active candidate."""
        logging.debug(f"update_by_uid(self, {uid}: str, {key}: str, {value}: Any)")
        if uid not in self._data:
            logging.debug(f"{uid} not in self.data. Return False")
            return False
     
        if key == "total":
            # Reset
            if value is None:
                setattr(self._data[uid], key, 0)
                setattr(self.candidates[uid], key, 0)

            # Increment
            else:
                curr_value = getattr(self._data[uid], key, value)
                logging.debug(f"curr_value={curr_value}")
                value = curr_value + value
        logging.debug(f"setattr(self._data[{uid}], {key}, {value})")
        setattr(self._data[uid], key, value)
        setattr(self.candidates[uid], key, value)

        return True
 
    def show(self) -> None:
        """Print and log state of the current active candidates."""
        msg = f"# --- Active Candidate Pool Size: ({len(self._data)}) --- #"
        logging.debug(msg)
        
        for idx, (_, candidate) in enumerate(self._data.items()):
            cand_info = f"  [{idx}] Active Candidate: {vars(candidate)}"
            logging.debug(cand_info)
           