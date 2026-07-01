# voting_systems/weighted_sys.py

"""
+----------------------------------------------------------------------------
| WEIGHTED VOTING SYSTEM
+----------------------------------------------------------------------------
| Score all voting systems and then assign weight to each one of them.  Then
| determine the placement of candidates by utilizing all systems.
| Note: If noise is added we randomize the weights to see if there are
| different results.
+----------------------------------------------------------------------------
"""

# Python Libraries
import logging
import random

# Local Libraries
from src.constants import (
    I_TROPHY, 
    VOTING_SYS,
    WEIGHTED_SYS_DEFAULT,
    )
from src.utils import name_len, show_banner
from voting_systems.base_voting_sys import BaseVotingSystem


class WeightedSystem(BaseVotingSystem):
    def __init__(self, candidates: dict, voters: dict, add_noise: bool=False):
        super().__init__(candidates, voters) 

        self.add_noise = add_noise
        self.title = "Weighted Voting" + self.title

    def results(self, all_candidates_data: dict) -> None:
        # Processes the all_candidates matrix to calculate consensus scores.
        logging.info("Calculating Weighted Consensus Matrix...")
       
        # Fetch live pool references
        # Note: The candidate pool and dicts of candidates are the same.
        candidates = self._pool.get()

        # Define num_candidates so your Borda math doesn't throw a NameError
        num_candidates = len(candidates)
        
        # Reset previous score attributes to 0.0 before calculating
        # Define trust matrix system weights (Must total 1.0 or scale relatively)
        weights = self._get_sys_weights()
        
        self.tally_totals(use_pool=True, clear_totals=True)
        
        for sys_name, system_pool in all_candidates_data.items():
            sys_weight = weights.get(sys_name, 1.0)
            
            # Safely convert any incoming pool variance or list profile into an object iterable
            if isinstance(system_pool, dict):
                cand_objects = list(system_pool.values())
            elif hasattr(system_pool, 'values'):
                cand_objects = list(system_pool.values())
            else:
                cand_objects = list(system_pool)
                
            # Sort them by their internal vote totals to establish finishing ranks
            sorted_snapshot = sorted(cand_objects, key=lambda c: c.total, reverse=True)
            
            for rank_idx, cand_snap in enumerate(sorted_snapshot):
                placement = rank_idx + 1
                base_points = (num_candidates - placement) + 1
                weighted_points = base_points * sys_weight
                
                # Extract the string UID explicitly to guarantee dictionary key matching succeeds
                target_uid = str(cand_snap.uid)
                
                # Add points to the live weighted tracking pool instances cleanly
                if target_uid in candidates:
                    candidates[target_uid].total += weighted_points
                    
        # Synchronize the updated live data dict back to the class property safely
        self.candidates = candidates

    def show_results(self) -> None:
        # Generates the master aligned multi-system score matrix visualization board.
        logging.info("# --- Displaying final candidate weighted scores ---#")
       
        candidates = self._pool.get()
        if not candidates:
            logging.warning("No weighted scoring data present.")
            return
            
        # Calculate the max length dynamically to protect padding columns from alignment drifts
        subtitles = []
        name_len_dict = name_len(candidates.values())
        max_name_len = name_len_dict["max"]
        
        # Sort the active pool by the newly accumulated .total score (highest score at top)
        sorted_candidates = sorted(candidates.values(), key=lambda c: c.total, reverse=True)
        winner = sorted_candidates[0]
        
        for rank, candidate in enumerate(sorted_candidates, 1):
            # Uses your nested f-string specifier formatting block to keep pipes perfectly straight
            line = f" Rank #{rank:<{3}} | Candidate: {candidate.name:<{max_name_len}} | Weighted Score: {candidate.total:.2f}"
            subtitles.append(line)
            logging.info(line)

        winner_line = f"Final Winner: {winner.name} ({winner.party}) | Score: {round(winner.total, 2)}".upper()
        logging.info(f"\n{I_TROPHY} {winner_line}\n")

        subtitles.append("\n")
        subtitles.append(winner_line)

        show_banner(self.title, subtitles)
        print(f"\n{I_TROPHY} {winner_line}\n")

    def _add_noise_weight(self, max_weight) -> float:
        if self.add_noise:
            noise = random.uniform(0, max_weight)
            return random.uniform(-noise, noise)

        return 0.0
    
    def _get_sys_weights(self) -> dict:
        sys_weights = {}
        
        # If noises is added random the order of the system and random noise to a default weight
        if self.add_noise:
            total_weight = 0
            voting_systems = random.sample(VOTING_SYS, len(VOTING_SYS))
            
            for sys_name in voting_systems:
                weight = WEIGHTED_SYS_DEFAULT + self._add_noise_weight((1 - total_weight) - WEIGHTED_SYS_DEFAULT)
                total_weight += weight
                sys_weights[sys_name] = weight
        else:
            # Use default valued weights added dynamically
            for sys_name in VOTING_SYS:
                const_name = f"WEIGHT_{sys_name}".upper()
                sys_weights[sys_name] = getattr(self.__class__.__name__, const_name, WEIGHTED_SYS_DEFAULT)

        logging.info(f"Voting System Weights: {sys_weights}")
        return sys_weights
