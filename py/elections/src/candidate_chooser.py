# src/candidate_chooser.py

# Python Libraries
import logging
import random
import sys

# Local Libraries
from src.candidate import Candidate
from src.constants import (
    ELECTION_DURATION,
    FIRST_CHOICE,
    I_FLAG,
    PARTY_BTM_TIER,
    PARTY_MID_TIER,
    PARTY_TOP_TIER, 
    PERCENTILE, 
    VOTE_BLANK,
    VOTE_BLANK_PCT_THRESH,
    VOTE_BY_LIKELYNESS_ODDS,
    VOTE_METHODICAL_ODDS,
    VOTE_NOISE_ODDS, 
)
from src.utils import get_index_by_uid

class CandidateChooser:
    def __init__(self, 
    candidates: list, 
    total_donations: float, 
    party_counts: dict,
    mean_name_len: int,
    add_noise: bool=False,
    ):
        logging.debug("# --- CandidateChooser() instantiated --- #")

        self.add_noise = add_noise
        self.candidates = candidates # public
        self.mean_name_len = mean_name_len
        self.party_counts = party_counts
        self.total_donations = round(total_donations, 2)

        # Build favorables once at the beginning to get the odds.
        self.favorables_orig = self.get_favorables()
        self.favorables = self.favorables_orig.copy()
        
        logging.debug(f"favorables count = {len(self.favorables)}")

        if len(self.favorables) == 0:
            logging.critical("No favorables found.  Debug!")
            logging.critical("Checking for candidates")
            logging.critical(f"candidates = {self.candidates}")
            logging.critical("sys.exit(0)")
            sys.exit(0)
  
    # --- Voter decision --- #

    def decision(self) -> str | None:
        # Three options: No vote, if there is a vote a random vote, if a methodical vote either favorability or heuristic
        candidate_uid = None
        decision_odds = random.randint(0, PERCENTILE)
        logging.debug(f"decision odds: {decision_odds}")

        if self.add_noise and decision_odds <= VOTE_BLANK_PCT_THRESH: # 15% odds
            candidate_uid = self._choose_none()
        else: # 85% odds
            #decision_odds = random.randint(0, PERCENTILE)
            # Voter is going to make a choice...
            if decision_odds <= VOTE_BY_LIKELYNESS_ODDS: # 12% odds
                # Voter is just going to vote randomly due to unfamiliarity or apathy.
                candidate_uid = self._choose_anyone()
            else: # 88% odds
                candidate_uid = self._choose_favorable(decision_odds)

            # log error
            if candidate_uid is None:
                logging.error(f"{I_FLAG} Methodologial decision retuned no candidate!")
                
        return candidate_uid
        
    def _choose_none(self) -> None:
        logging.debug("choose_none()")
        return VOTE_BLANK

    def _choose_anyone(self) -> str:
        logging.debug("choose_anyone()")
        candidate = random.choice(self.candidates)
        return candidate.uid

    def _choose_favorable(self, decision_odds: int) -> str:
        logging.debug("_choose_favorable()")
        methodical_odds = VOTE_METHODICAL_ODDS
                 
        # Add 10% decision complexity for realism
        if self.add_noise:
            noise_min_diff = ((VOTE_NOISE_ODDS * VOTE_METHODICAL_ODDS) * -1) # -10%
            noise_max_diff = VOTE_NOISE_ODDS * VOTE_METHODICAL_ODDS # +10% 
            methodical_odds = random.uniform(noise_min_diff, noise_max_diff)
            
        # Starts at 50/50
        if decision_odds < methodical_odds: # 50% odds (with noise 40-60%)
            candidate_uid = self._choose_by_favorability()
        else:
            candidate_uid = self._choose_by_heuristic()

        return candidate_uid

    def _choose_by_favorability(self) -> str:
        logging.debug("_choose_by_favorability()")
        # Option 1: Treat as favorability: Take scoress of all candidates, sort by highest as choose order.
        # Sort by score.

        if len(self.favorables):
            sorted_favorables = sorted(self.favorables, key=lambda x: x["score"], reverse=True)
         
            return sorted_favorables[FIRST_CHOICE].get("uid") 
        else:
            logging.error("There are no candidates in pool!")
            return None
        
    def _choose_by_heuristic(self) -> str:
        logging.debug("_choose_by_heuristic()")

        # Option 2: Take score aka percentages, stack the percentages and pick a random number to determine which 
        # stack to choose from (more intuitive).

        # To choose by heuristic, you apply a mental shortcut or "rule of thumb" to make a decision quickly without 
        # needing to analyze every piece of data. It provides a "good enough" answer in a fraction of the time.
        
        logging.debug(f"check `thresh` in self.favorables: {(self.favorables)}")
        
        candidate_chosen = None
        max_thresh_dict = max(self.favorables, key=lambda x: x["thresh"])
        max_threshold = max_thresh_dict.get("thresh")
        choose_threshold = random.randint(0, max_threshold)
        logging.debug(f"choose_threshold = {choose_threshold}")

        for candidate in self.favorables:
            if choose_threshold <= candidate.get("thresh"):
                candidate_chosen = candidate.get("uid")
                logging.info(f"Choosing {candidate_chosen} by a heuristic approach.")
                break
    
        if candidate_chosen is None:
            logging.error("No candidate chosen!")

        return candidate_chosen

    # --- Likelihood --- #
   
    def get_favorables(self) -> list:
        logging.debug('get_favorables()')
        return self._calc_favorables()

    def _calc_favorables(self) -> dict:
        logging.debug('_calc_favorables()')
        # Logic to pick a candidate.  Party, Gender name, placement on the ballot, campaign donations, 
        # duration of candidacy
        favorables = []
        thresh = 0
        for candidate in self.candidates:
            favorables_data = self._rank_candidate(candidate)
            thresh = thresh + int(round(favorables_data["score"], 0))
            favorables_data["thresh"] = thresh
  
            favorables_dict = {
                "uid": candidate.uid,
                "score": favorables_data["score"],
                "thresh": favorables_data["thresh"]
            }

            #logging.debug(f"favorables_dict = {favorables_dict}")
            favorables.append(favorables_dict)
        logging.debug(f"favorables = {favorables}")
        return favorables

    def _get_favorables_score(self, favorables_data: dict) -> int:
        score = 0
        for key in favorables_data:
            score += round(favorables_data[key], 2)
          
        return score

    def sync_favorables(self) -> None:
        logging.debug("sync_favorables()")
        # Whatever candidates are left in the pool need to match the favorable choices
        synced = []
        current = self.favorables

        for curr in current:
            for candidate in self.candidates:
                if candidate.uid == curr.get("uid"):
                    synced.append(curr)

        logging.debug(f"favorables synced: {synced}")
        self.favorables = synced

    def reset_favorables(self) -> None:
        logging.debug("reset_favorables()")
        if self.favorables == self.favorables_orig:
            logging.debug("favorables == orig")
      
        self.favorables = self.favorables_orig.copy()

    # --- Ranking Functions --- #

    def _rank_candidate(self, candidate: Candidate) -> dict:
        logging.debug(f"(Rank) Candidate: {candidate.uid}")
        party_val, party_weight = self._rank_party(candidate.party, self.party_counts[candidate.party])
        duration_val, duration_weight = self._rank_duration(candidate.duration)
        donation_val, donation_weight = self._rank_donations(candidate.donations)
        ballot_placement_val, ballot_placement_weight = self._rank_placement_on_ballot(candidate.uid)
        name_val, name_weight = self._rank_name(candidate.name)

        favorables_data = {
            "party": party_val * party_weight,
            "duration": duration_val * duration_weight,
            "donation": donation_val * donation_weight,
            "ballot_placement": ballot_placement_val * ballot_placement_weight,
            "name": name_val * name_weight
        }

        favorables_data["score"] = round(self._get_favorables_score(favorables_data), 2)

        return favorables_data

    def _rank_party(self, party: str, party_cnt: int=1) -> tuple(float, int): 
        # If Democrat 48/100, Republican 48/100, Green 4/100, Constitution 1/100m 
        # Libertarian 2/100, Progressive 1/100m , Reform 0.5/100
        weight = 40

        if party in ['Democrat', 'Republican']:
            points = (PARTY_TOP_TIER + random.uniform(0, 0.9)) + self._add_party_noise(PARTY_TOP_TIER)
        elif party == 'Green':
            points = (PARTY_MID_TIER + random.uniform(0, 0.9)) + self._add_party_noise(PARTY_MID_TIER)
        elif party == 'Libertarian':
            points = (PARTY_BTM_TIER + random.uniform(0, 2)) + self._add_party_noise(PARTY_BTM_TIER)
        else:
            points = random.uniform(0.33, 1) + self._add_party_noise(1)

        logging.debug(f"Raw points = {points}")
        points = ((points / party_cnt) / PERCENTILE)
        logging.debug(f"_rank_party({party}): party_cnt={party_cnt}, points={points}, weight={weight} ")
        return points, weight

    def _add_party_noise(self, tier: int=0) -> float:
        ten_pct_noise = .10 * tier
        return random.uniform(-1 * ten_pct_noise, ten_pct_noise) if self.add_noise else 0

    def _rank_duration(self, duration: int) -> tuple(float, int):
        # Longer the duration the higher the donation, media attention
        weight = 20
        pct = duration / ELECTION_DURATION
        logging.debug(f"_rank_duration({duration}): pct={pct}, weight={weight}")
        return pct, weight

    def _rank_donations(self, donations: float) -> tuple(float, int):
        # Higher the more likely to pick
        weight = 25
        pct = (donations / self.total_donations)
        logging.debug(f"_rank_donations({donations}) pct={pct}, weight={weight}")
        return pct, weight
    
    def _rank_placement_on_ballot(self, uid: str) -> tuple(float, int):  

        # Calculate percentile aka rank
        weight = 10
        index = get_index_by_uid(self.candidates, uid)
        place = index + 1
        percentile_formula = (1 - (place - 1) / (len(self.candidates) - 1)) 
        logging.debug(f"_rank_placement_on_ballot({uid}): pct={percentile_formula}, weight={weight}")

        return round(percentile_formula, 1), weight
        
    def _rank_name(self, name: str) -> int: 
        weight = 5

        # The longer the name the harder to pronounce the least likely to vote for that andidate
        if len(name) > self.mean_name_len:
            logging.debug(f"_rank_name():  0, weight={weight}")
            return 0, 1
        logging.debug(f"_rank_name():  1, weight={weight}")
        return 1, weight
