# src/candidate_chooser.py

# Python Libraries
import logging
import random
import sys

# Local Libraries
from src.candidate import Candidate
from src.constants import (
    CANDIDATE_WEIGHT_BALLOT_PLACEMENT,
    CANDIDATE_WEIGHT_DONATION,
    CANDIDATE_WEIGHT_DURATION,
    CANDIDATE_WEIGHT_NAME,
    CANDIDATE_WEIGHT_PARTY,
    ELECTION_DURATION,
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
    WEIGHT_NOISE, 
)
from src.utils import name_len
 

class CandidateChooser:
    def __init__(self, 
    candidates: dict, 
    total_donations: float, 
    party_counts: dict,
    add_noise: bool=False,
    ):
        logging.debug("# --- CandidateChooser() instantiated --- #")
        
        self.add_noise = add_noise
        self.candidates = candidates # public

        self._name_len = name_len(self.candidates.values())
        self._party_counts = party_counts
        self._total_donations = round(total_donations, 2)
        self._favorables_orig = self.get_favorables()
        self._favorables = self._favorables_orig.copy()

        self._check_favorables()

    # --- Voter decision --- #
    def decision(self) -> str | None:
        # Three options: No vote, if there is a vote a random vote, if a methodical vote either favorability or heuristic.
        self._check_favorables()

        candidate_uid = None
        decision_odds = random.randint(0, PERCENTILE)
        logging.debug(f"decision_odds: {decision_odds}")

        if self.add_noise and decision_odds <= VOTE_BLANK_PCT_THRESH: # 15% odds
            candidate_uid = self._choose_none()
        else: # 85% odds
            
            # If we're adding noise, lets get a new decision odds
            if self.add_noise:
                if (random.choice([0,1])) == 0:
                    decision_odds = random.randint(0, PERCENTILE)

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
        return VOTE_BLANK

    def _choose_anyone(self) -> str:
        # Grab all the UID string keys directly as a list
        uids = list(self.candidates)
    
        # Pick a random choice safely if the list isn't empty
        if uids:
            return random.choice(uids)
            
        return None

    def _choose_favorable(self, decision_odds: int) -> str:
        methodical_odds = VOTE_METHODICAL_ODDS
                 
        # Add 10% decision complexity for realism
        if self.add_noise:
            noise_diff = VOTE_NOISE_ODDS * VOTE_METHODICAL_ODDS # +10% 
            methodical_odds = random.uniform(-noise_diff, noise_diff)
            
        # Starts at 50/50
        if decision_odds < methodical_odds: # 50% odds (with noise 40-60%)
            candidate_uid = self._choose_by_favorability()
        else:
            candidate_uid = self._choose_by_heuristic()

        return candidate_uid

    def _choose_by_favorability(self) -> str:
        # Option 1: Treat as favorability: Take scoress of all candidates, sort by highest as choose order.
        # Sort by score.
        if len(self._favorables):
             
            max_favorability_uid, _ = max(self._favorables.items(), key=lambda x: x[1]["score"])

            return max_favorability_uid
        else:
            logging.error("Error: There are no candidates in the pool❗")
            return
        
    def _choose_by_heuristic(self) -> str:
        # Option 2: Take score aka percentages, stack the percentages and pick a random number to determine which 
        # stack to choose from (more intuitive).

        # To choose by heuristic, you apply a mental shortcut or "rule of thumb" to make a decision quickly without 
        # needing to analyze every piece of data. It provides a "good enough" answer in a fraction of the time.
        candidate_chosen = None
        choose_threshold = self._get_choose_threshold()

        for uid, favorable_data in self._favorables.items():
            if choose_threshold <= favorable_data["thresh"]:
                candidate_chosen = uid
                logging.info(f"Choosing {candidate_chosen} by a heuristic approach.")
                break
    
        if candidate_chosen is None:
            logging.error("No candidate chosen❗")
        
        return candidate_chosen

    # --- Likelihood --- #
    
    def _get_choose_threshold(self) -> int:

        # Provide an empty tuple pair as a safe default to prevent crashing
        favorables_by_thresh = max(
            self._favorables.items(), 
            key=lambda x: x[1]["thresh"], 
            default=(None, None)
        )
        
        _, favorable_data = favorables_by_thresh
        
        # Guard against an empty dictionary
        if favorable_data is None:
            return 0  # Or whatever fallback integer your function expects
            
        # Pull the actual integer values out cleanly by their key names
        max_thresh = favorable_data["thresh"]
        
        return random.randint(0, int(max_thresh))
   
    def get_favorables(self) -> list:
        return self._calc_favorables()

    def _calc_favorables(self) -> dict:
        # Logic to pick a candidate.  Party, Gender name, placement on the ballot, campaign donations, 
        # duration of candidacy
        thresh = 0
        favorables = {}
        for uid, candidate in self.candidates.items():
            favorables_data = self._rank_candidate(candidate)
            thresh = thresh + favorables_data["score"]
        
            favorables_dict = {
                "score": favorables_data["score"],
                "thresh": int(thresh)
            }

            favorables[uid] = favorables_dict

        return favorables

    def _get_favorables_score(self, favorables_data: dict) -> int:
        return sum(round(favorables_data[key], 2) for key in favorables_data)

    def sync_favorables(self) -> None:
        # Whatever candidates are left in the pool need to match the favorable choices
        synced = {}
        for favorable_uid, favorable in self._favorables.items():
            for candidate_uid, _ in self.candidates.items():
                if candidate_uid == favorable_uid:
                    synced[favorable_uid] = favorable

        self._favorables = synced

    def reset_favorables(self) -> None:
        self._favorables = self._favorables_orig.copy()

    # --- Ranking Functions --- #

    def _rank_candidate(self, candidate: Candidate) -> dict:
        party_val = self._rank_party(candidate.party, self._party_counts[candidate.party])
        duration_val = self._rank_duration(candidate.duration)
        donation_val = self._rank_donations(candidate.donations)
        ballot_placement_val = self._rank_placement_on_ballot(candidate.uid)
        name_val = self._rank_name(candidate.name)

        favorables_data = {
            "party": party_val * CANDIDATE_WEIGHT_PARTY,
            "duration": duration_val * CANDIDATE_WEIGHT_DURATION,
            "donation": donation_val * CANDIDATE_WEIGHT_DONATION,
            "ballot_placement": ballot_placement_val * CANDIDATE_WEIGHT_BALLOT_PLACEMENT,
            "name": name_val * CANDIDATE_WEIGHT_NAME
        }

        favorables_data["score"] = round(self._get_favorables_score(favorables_data), 2)

        return favorables_data

    def _add_party_noise(self, tier: int=0) -> float:
        ten_pct_noise = WEIGHT_NOISE * tier
        return random.uniform(-ten_pct_noise, ten_pct_noise) if self.add_noise else 0

    def _rank_party(self, party: str, party_cnt: int=1) -> float: 
        """
        Odds of party ranking:
        ----------------------
        - Democrat:     48/100
        - Republican:   48/100
        - Green:        4/100
        - Constitution: 1/100 
        - Libertarian:  2/100
        - Progressive:  1/100
        - Reform:       0.5/100
        """
     
        if party in ["Democrat", "Republican"]:
            points = (PARTY_TOP_TIER + random.uniform(0, 1)) + self._add_party_noise(PARTY_TOP_TIER)
        elif party == ["Green", "Socialist of America"]:
            points = (PARTY_MID_TIER + random.uniform(0, 0.5)) + self._add_party_noise(PARTY_MID_TIER)
        elif party == "Libertarian":
            points = (PARTY_BTM_TIER + random.uniform(0, 2)) + self._add_party_noise(PARTY_BTM_TIER)
        else:
            points = random.uniform(0.33, 1) + self._add_party_noise(1)

        points = ((points / party_cnt) / PERCENTILE)
        logging.debug(f"_rank_party({party}): party_cnt={party_cnt}, points={points}, weight={CANDIDATE_WEIGHT_PARTY}, points={points} ")
        return points

    def _rank_duration(self, duration: int) -> float:
        # Longer the duration the higher the donation, media attention
        pct = duration / ELECTION_DURATION
        logging.debug(f"_rank_duration({duration}): pct={pct}, weight={CANDIDATE_WEIGHT_DURATION}")
        return pct

    def _rank_donations(self, donations: float) -> float:
        # Higher the more likely to pick
        pct = (donations / self._total_donations)
        logging.debug(f"_rank_donations({donations}) pct={pct}, weight={CANDIDATE_WEIGHT_DONATION}")
        return pct
    
    def _rank_placement_on_ballot(self, uid: str) -> float:  
        # Calculate percentile aka rank
        index = None
        for idx, (candidate_uid, _) in enumerate(self.candidates.items()):
            if uid == candidate_uid:
                index = idx
                break

        if not index:
            return 0.0

        place = index + 1
        percentile_formula = (1 - (place - 1) / (len(self.candidates) - 1))
        logging.debug(f"_rank_placement_on_ballot({uid}): pct={percentile_formula}, weight={CANDIDATE_WEIGHT_BALLOT_PLACEMENT}, place={place}")
        return round(percentile_formula, 1)

    def _rank_name(self, name: str) -> int: 
        # The longer the name the harder to pronounce the least likely to vote for that andidate
        return 0 if len(name) > self._name_len["mean"] else 1

    def _check_favorables(self) -> None:
        if len(self._favorables) == 0:
            logging.critical(f"No favorables found!\nCandidate count: {len(self.candidates)}")
            logging.critical("sys.exit(0)")
            sys.exit(0)
        