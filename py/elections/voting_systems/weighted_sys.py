# voting_systems/weighted_sys.py

"""
+----------------------------------------------------------------------------
| WEIGHTED VOTING SYSTEM
+----------------------------------------------------------------------------
| Score all voting systems and then assign weight to each one of them.  Then
| determine the placement of candidates by utilizing all systems.
|
+----------------------------------------------------------------------------
"""

import logging
import random
from src.constants import FIRST_CHOICE, I_RIBBON, I_TROPHY, WEIGHTED_SYS_DEFAULT
from src.utils import draw_line, show_banner
from voting_systems.base_voting_sys import BaseVotingSystem


class WeightedSystem(BaseVotingSystem):
    def __init__(self, candidates: dict, voters: dict):
        super().__init__(candidates, voters) 
        
        self.title = "Weighted Voting" + self.title
        self.add_noise = False

    def results_old(self, candidates: dict, add_noise: bool=False):
        self.add_noise = add_noise
        self._pool.reset()
        
        SYS_TOTAL_WEIGHT = 1
        SYS_WEIGHT = 0.25

        choice = FIRST_CHOICE           
        total_weight = 0
        while total_weight < SYS_TOTAL_WEIGHT:
            for uid, candidate in candidates.items():
                weight = SYS_WEIGHT + self._add_weight_noise()
                candidate["weight"] = weight
                total_weight += weight

        for uid, candidates in candidates.items():
            sorted_candidates = dict(
                sorted(
                    candidates.items(), 
                    key=lambda item: item[1]["total"], 
                    reverse=True
                )
            )

            for candidate in sorted_candidates:

                percentile = 0
                candidate["percentile"] = self._calc_percentile(candidate)

                
            #candidates = self._pool.get()

        
        # Which candidate did the best out of all the systems.


    def _add_noise_weight(self, max_weight) -> float | int:
        if self.add_noise:
            #SYS_WEIGHT = 0.25
            noise = random.uniform(0, max_weight)
            return random.uniform(-1 * noise, noise)

        return 0.0

    
    def results(self, all_candidates_data: dict, add_noise: bool = False) -> None:
        """
        Processes the all_candidates matrix to calculate consensus scores.
        """
        logging.info("Calculating Weighted Consensus Matrix...")
        
        # Define trust matrix system weights (Must total 1.0 or scale relatively)
        self.add_noise = add_noise
        if self.add_noise:
            total_weight = 0
            weights = {}
            for sys_name in ["popular", "ranked", "redist", "remaining"]:
                weight = WEIGHTED_SYS_DEFAULT + self._add_noise_weight((1 - total_weight) - WEIGHTED_SYS_DEFAULT)
                total_weight += weight
                weights[sys_name] = weight
        else:
            weights = {
                "popular": 0.20,
                "ranked": 0.40,  # Higher trust for Ranked-Choice preference accuracy
                "redist": 0.20,
                "remaining": 0.20
            }
        print(weights)
        
        # 1. Fetch live pool references
        candidates = self._pool.get()
        
        # Define num_candidates so your Borda math doesn't throw a NameError
        num_candidates = len(candidates)
        
        # Reset previous score attributes to 0.0 before calculating
        for candidate in candidates.values():
            candidate.total = 0.0

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
                
                if target_uid in candidates:
                    # Add points to the live weighted tracking pool instances cleanly
                    candidates[target_uid].total += weighted_points
                    
        # Synchronize the updated live data dict back to the class property safely
        self.candidates = candidates

    def show_results(self) -> None:
        """Generates the master aligned multi-system score matrix visualization board."""
        logging.info("Displaying final weighted scores.")
        subtitles = []


        candidates = self._pool.get()
        if not candidates:
            logging.warning("No weighted scoring data present.")
            return
            
        # Calculate the max length dynamically to protect padding columns from alignment drifts
        max_name_len = max(len(c.name) for c in candidates.values())
        
        # Sort the active pool by the newly accumulated .total score (highest score at top)
        sorted_candidates = sorted(candidates.values(), key=lambda c: c.total, reverse=True)
        winner = sorted_candidates[0]
        
        for rank, candidate in enumerate(sorted_candidates, 1):
            # Uses your nested f-string specifier formatting block to keep pipes perfectly straight
            line = f" Rank #{rank} | Candidate: {candidate.name:<{max_name_len}} | Weighted Score: {candidate.total:.2f}"
             
            subtitles.append(line)
            logging.info(line)

        

        winner_line = f"Final Winner: {winner.name} ({winner.party}) | Score: {round(winner.total, 2)}".upper()
        logging.info(f"\n{I_TROPHY} {winner_line}\n")
        subtitles.append("\n")
        subtitles.append(winner_line)

        show_banner(self.title, subtitles)
        print(f"\n{I_TROPHY} {winner_line}\n")
    