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
    PARTY_BTM_TIER,
    PARTY_MID_TIER,
    PARTY_TOP_TIER, 
    #MAX_VOTER_CANDIDATE_SCORE, 
    PERCENTILE, 
    POLITICAL_PARTIES,
    VOTER_LIKELYNESS_PICK_ODDS, 
)
from src.utils import get_index_by_uid

class CandidateChooser:
    def __init__(self, 
    candidates: list, 
    total_contributions: float, 
    mean_name_len: int,
    add_noise: bool=False,
    ):
        logging.debug("CandidateChooser() instantiated")
        self.add_noise = add_noise
        self.candidates = candidates
        self.mean_name_len = mean_name_len
        self.party_counts = self._count_parties()
        self.total_contributions = round(total_contributions, 2)

        # Build likeliness once at the beginning to get the odds.
        self.likeliness_orig = self.get_likeliness()
        self.likeliness = self.likeliness_orig.copy()
        
        logging.debug(f"likeliness count = {len(self.likeliness)}")
  
    def pick(self, candidate_pool: list) -> str:
        # Logic to pick candidate from candidate pool
        # Pick the likeliness that a voter will just pick a random candidate out of fatigue or a lack of information
        # Then pick a random number.  If that number is less than the likelness pick a random candidate from the candidate pool.
        # Otherwise, use voter logic to determine who they're most likely to pick
        self.candidates = candidate_pool.copy()

        # Sync likeability candidates
        self._sync_likeliness()

        #logging.debug("pick()")
        #logging.debug(f"pick() Current Candidate Pool")
        #for c in self.candidates:
        #    logging.debug(f"candidate = {vars(c)}")

        # --- DO WE WANT TO PICK (random guess) OR CHOOSE (methodolical decision) A CANDIDATE? --- #

        pick_random_candidate_likeliness = random.randint(0, VOTER_LIKELYNESS_PICK_ODDS)
        random_pick = random.randint(0, PERCENTILE)
        
        logging.debug(f'Random candidate likeliness: {pick_random_candidate_likeliness}, random_pick: {random_pick}')
        random_pick = 99
        if random_pick <= pick_random_candidate_likeliness:
            random_candidate = random.choice(self.candidates)
            candidate_uid = random_candidate.uid
            logging.info(f'Picking random candidate {candidate_uid}')

        else:
            # Choose a candidate by likeability or a heuristic approach.
            # Randomly choose 50/50 whether to use the likeability or heuristic approach.
            candidate_uid = self._choose_by_heuristic() if random.randint(0, 1) == 1 else self._choose_by_likeability()
            
        # Now that we have our chosen candidate remove them from the pool and return them to the elector for counting.
        #self._refresh_likeliness(candidate_uid)

        return candidate_uid

    def get_likeliness(self) -> list:
        logging.debug('get_likeliness()')
        return self._calc_likeliness()

    def reset_likeliness(self) -> None:
        self.likeliness = self.likeliness_orig.copy()

    def _sync_likeliness(self) -> None:
        logging.debug("Syncing likeliness...")
        synced = []
        current = self.likeliness.copy()
        
        for curr in current:
            #logging.debug(f"curr: {curr}")
            for candidate in self.candidates:
                #logging.debug(f"candidate: {candidate}")
                if candidate.uid == curr.get("uid"):
                    synced.append(curr)
        logging.debug(f"likeliness synced: {synced}")
        self.likeliness = synced

    def _refresh_likeliness_orig(self, candidate_chosen: str) -> None:
        # remove chosen candidates from 
        logging.debug(f"Before -> likeliness count = {len(self.likeliness)}")
        logging.debug(f"Removing all {candidate_chosen} from likeliness.")

        filtered = [candidate for candidate in self.likeliness if candidate["uid"] != candidate_chosen]
        self.likeliness = filtered
      
        logging.debug(f"After -> likeliness count = {len(self.likeliness)}")

    def _rank_candidate(self, candidate: Candidate) -> dict:
        party_val, party_weight = self._rank_party(candidate.party, self.party_counts[candidate.party])
        duration_val, duration_weight = self._rank_duration(candidate.duration)
        contribution_val, contribution_weight = self._rank_contributions(candidate.contributions)
        ballot_placement_val, ballot_placement_weight = self._rank_placement_on_ballot(candidate.uid)
        name_val, name_weight = self._rank_name(candidate.name)

        likeliness_data = {
            "party": party_val * party_weight,
            "duration": duration_val * duration_weight,
            "contribution": contribution_val * contribution_weight,
            "ballot_placement": ballot_placement_val * ballot_placement_weight,
            "name": name_val * name_weight
        }

        likeliness_data["score"] = self._get_likeliness_score(likeliness_data)

        return likeliness_data

    def _calc_likeliness(self) -> dict:
        # Logic to pick a candidate.  Party, Gender name, placement on the ballot, campaign contributions, 
        # duration of candidacy
        likeliness = []
        thresh = 0
        for candidate in self.candidates:
            logging.debug("\n")
            likeliness_data = self._rank_candidate(candidate)

            """
            party_val, party_weight = self._rank_party(candidate.party, self.party_counts[candidate.party])
            duration_val, duration_weight = self._rank_duration(candidate.duration)
            contribution_val, contribution_weight = self._rank_contributions(candidate.contributions)
            ballot_placement_val, ballot_placement_weight = self._rank_placement_on_ballot(candidate.uid)
            name_val, name_weight = self._rank_name(candidate.name)

            likeliness_data = {
                'party': party_val * party_weight,
                'duration': duration_val * duration_weight,
                'contribution': contribution_val * contribution_weight,
                'ballot_placement': ballot_placement_val * ballot_placement_weight,
                'name': name_val * name_weight
            }
            """

            #score = self._get_likeliness_score(likeliness_data)
            thresh = thresh + int(round(likeliness_data["score"], 0))
            #likeliness_data["score"] = score
            likeliness_data["thresh"] = thresh

            # below

            #likeliness_data["score"] = self._get_likeliness_score(likeliness_data)
            #thresh = thresh + likeliness_data["score"]
            #likeliness_data["thresh"] = thresh
            #score_sum += score
  
            likeliness_dict = {
                "uid": candidate.uid,
                "score": likeliness_data["score"],
                "thresh": likeliness_data["thresh"]
            }

            logging.debug(f"likeliness_dict = {likeliness_dict}")
            likeliness.append(likeliness_dict)
        
        return likeliness

    def _get_likeliness_score(self, likeliness_data: dict) -> int:
        score = 0
        for key in likeliness_data:
            score += likeliness_data[key]
            logging.debug(f"key={key}, new score = {score}")
        return score

    def _choose_by_likeability(self) -> str:
        logging.debug("_choose_by_likeability()")
        # Option 1: Treat as likeability: Take scoress of all candidates, sort by highest as choose order.
        # Sort by score.
        sorted_likeliness = sorted(self.likeliness, key=lambda x: x["score"], reverse=True)
        logging.info(f"Sorted likeliness: {sorted_likeliness}")
        #logging.info(f"Choosing {sorted_likeliness[0].get("uid")} by likeability.")
        return sorted_likeliness[FIRST_CHOICE].get("uid") 


    def _choose_by_heuristic(self) -> str | None:
        from operator import itemgetter, attrgetter

        logging.debug("_choose_by_heuristic()")
        # Option 2: Take score aka percentages, stack the percentages and pick a random number to determine which 
        # stack to choose from (more intuitive).

        # To choose by heuristic, you apply a mental shortcut or "rule of thumb" to make a decision quickly without 
        # needing to analyze every piece of data. It provides a "good enough" answer in a fraction of the time.
        
        candidate_chosen = None
        max_thresh_dict = max(self.likeliness, key=lambda x: x["thresh"])
        max_threshold = max_thresh_dict.get("thresh")
        #max(self.likeliness, key=lambda x: x["thresh"])
        logging.debug(f"max_threshold={max_threshold}")
        choose_threshold = random.randint(0, max_threshold - 1)
        logging.debug(f"choose_threshold = {choose_threshold}")

        #thresh = 0 
        for idx, candidate in enumerate(self.likeliness):
            #thresh = thresh + int(round(candidate["score"], 0))
            #logging.debug(f"idx={idx}, uid={candidate['uid']}, score={candidate['score']}")
            #candidate["thresh"] = thresh
            #logging.debug(f"if {choose_threshold} <= {thresh}: ")
            if choose_threshold <= candidate.get("thresh"):
                candidate_chosen = candidate.get("uid") #candidate["uid"]
                logging.info(f"Choosing {candidate_chosen} by a heuristic approach.")
                break
        logging.debug(f"self.likeliness={self.likeliness}")
        if candidate_chosen is None:
            logging.error("No candidate chosen!")

        return candidate_chosen

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
        # Longer the duration the higher the contribution, media attention
        weight = 20
        pct = duration / ELECTION_DURATION
        logging.debug(f"_rank_duration({duration}): pct={pct}, weight={weight}")
        return pct, weight

    def _rank_contributions(self, contributions: float) -> tuple(float, int):
        # Higher the more likely to pick
        weight = 25
        pct = (contributions / self.total_contributions)
        logging.debug(f"_rank_contributions({contributions}) pct={pct}, weight={weight}")
        return pct, weight
    
    def _rank_placement_on_ballot(self, uid: str) -> tuple(float, int):  

        # Calculate percentile aka rank
        weight = 10
        index = get_index_by_uid(self.candidates, uid)
        logging.debug(f"index={index}, uid={uid}")
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

    def _count_parties(self) -> dict:
        party_cnts = {}

        for party in POLITICAL_PARTIES:
            party_cnts[party] = 0

            for candidate in self.candidates:
                if candidate.party == party:
                    party_cnts[party] += 1
   
        return party_cnts
