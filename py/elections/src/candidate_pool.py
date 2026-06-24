# src/candidate_pool.py

import logging

from src.candidate import Candidate
# @todo - might not need
class CandidatePool:
    def __init__(self, candidates: list) -> None:
        self._candidates = candidates
        self.pool = self.reset()

    def add(self, candidate: Candidate) -> None: 
        # Add a candidate to pool
        self.pool.append(candidate)

    def clear(self) -> list:
        return []

    def get_candidates(self) -> list:
        return self._candidates

    @property
    def length(self) -> int:
        return len(self.pool)

    def remove(self, candidate: Candidate):
        # Remove a candidate from pool
        self.pool.remove(candidate)

    def reset(self) -> None:
        # Adds all candidates to pool
        self.pool = self.clear()
        for candidate in self._candidates:
            self.pool.append(candidate)

    # Sync in
    def update(self, candidates: list) -> None:
        # Syncs candidates with the candidates remaining in the pool.
        # Updates self.pool()
        # Use this after election is over
        self._candidates = candidates
        for candidate in candidates:
            for c_pool in self.pool:
                if c_pool.uid == candidate.uid:
                    c_pool = candidate

    # Sync out  
    def refresh(self) -> list:
        # Syncs remaining pool candidates with candiates
        _pool = self.clear()
        for c_pool in self.pool:
            for candidate in self._candidates:
                if c_pool.uid == candidate.pool:
                    candidate = c_pool
                    _pool.add(candidate)

        return _pool
