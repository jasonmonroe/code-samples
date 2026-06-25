# src/candidate_chooser.py

# Python Libraries
import logging
import random
import sys

# Local Libraries
from src.constants import (
    ELECTION_DURATION, 
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
        self.candidates = candidates
        self.total_contributions = round(total_contributions, 2)
        self.mean_name_len = mean_name_len
        self.party_counts = self._count_parties()
        self.add_noise = add_noise

        # Build likeliness once at the beginning to get the odds.
        self.likeliness_orig = self.get_likeliness()
        self.likeliness = self.likeliness_orig.copy()
        
        logging.debug(f"likeliness count = {len(self.likeliness)}")
  
    def pick(self, candidate_pool: list) -> str:
        # Logic to pick candidate from candidate pool
        # Pick the likeliness that a voter will just pick a random candidate out of fatigue or a lack of information
        # Then pick a random number.  If that number is less than the likelness pick a random candidate from the candidate pool.
        # Otherwise, use voter logic to determine who they're most likely to pick
        self.candidates = candidate_pool
        pick_random_candidate_likeliness = random.randint(0, VOTER_LIKELYNESS_PICK_ODDS)
        random_pick = random.randint(0, PERCENTILE)

        random.shuffle(self.likeliness)

        logging.debug(f'Random candidate likeliness: {pick_random_candidate_likeliness}, random_pick:{random_pick}')

        if random_pick <= pick_random_candidate_likeliness:
            random_candidate = random.choice(self.candidates)
            random_uid = random_candidate.uid
            logging.info(f'Picking random candidate {random_uid}')

        else:
            # Either pick max score OR create a list of 100 with number of indices based on the score, the higher the score the candidaete, the higher
            # the representation of indices.  Then pick a random number
            random_uid = random.choice(self.likeliness)
            logging.info(f'Choosing candidate {random_uid}')

        self._refresh_likeliness(random_uid)
        return random_uid

    def get_likeliness(self) -> list:
        likeliness = self._calc_likeliness()
        logging.debug('get_likeliness()')
        logging.debug(f"likeliness={likeliness}")

        return self._convert_to_list(likeliness)

    def reset_likeliness(self) -> None:
        self.likeliness = self.likeliness_orig.copy()

    def _refresh_likeliness(self, chosen: list) -> None:
        # remove chosen candidates from 
        logging.debug(f"Before -> likeliness count = {len(self.likeliness)}")
        logging.debug(f"Removing all {chosen} from likeliness.")

        filtered = [item for item in self.likeliness if item != chosen]
        self.likeliness = filtered
        random.shuffle(self.likeliness)

        logging.debug(f"After -> likeliness count = {len(self.likeliness)}")

    def _calc_likeliness(self) -> dict:
        # Logic to pick a candidate.  Party, Gender name, placement on the ballot, campaign contributions, 
        # duration of candidacy
        likeliness = []

        for candidate in self.candidates:
            """
            party_val, party_weight = self._rank_party(candidate.party, self.party_counts[candidate.party])
            duration_val, duration_weight = self._rank_duration(candidate.duration)
            contribution_val, contribution_weight = self._rank_contributions(candidate.contributions)
            ballot_placement_val, ballot_placement_weight = self._rank_placement_on_ballot(candidate.uid)
            name_val, name_weight = self._rank_name(candidate.name)
            """

            party_val, party_weight = self._rank_party(candidate.party, self.party_counts[candidate.party])
            duration_val, duration_weight = self._rank_duration(candidate.duration)
            contribution_val, contribution_weight = self._rank_contributions(candidate.contributions)
            ballot_placement_val, ballot_placement_weight = self._rank_placement_on_ballot(candidate.uid)
            name_val, name_weight = self._rank_name(candidate.name)


            likeliness_scores = {
                'party': party_val * party_weight,
                'duration': duration_val * duration_weight,
                'contribution': contribution_val * contribution_weight,
                'ballot_placement': ballot_placement_val * ballot_placement_weight,
                'name': name_val * name_weight
            }

            # Calculate score
            score = 0
            for key in likeliness_scores:
                score += likeliness_scores[key]
                
            likeliness_scores["score"] = score
            likeliness_scores["pct"] = ((score / PERCENTILE) * PERCENTILE)
  
            logging.debug(f'uid={candidate.uid}, likeliness_scores={likeliness_scores}')
            logging.debug(f'Score: {score}')
            likeliness.append({'uid': candidate.uid, 'score': score, 'pct': likeliness_scores["pct"]})

        return likeliness


     


    def _likeability_method(self):
        # Option 1: Treat as likeability: Take scoress of all candidates, sort by highest as choose order.
        pass

    def _intuitive_method(self):
        # Option 2: Take percentages, stack the percentages and pick a random number to determine which 
        # stack to choose from (more intuitive).
        pass

        
    # @todo - redo this logic.  Need a better way to get the likeliness!
    def _convert_to_list(self, likeliness: dict) -> list:
        candidate_likeliness = []
        
        for candidate in likeliness:
            uid = candidate["uid"]
            pct = candidate["pct"]
            cnt = int(pct * 10)
            logging.debug(f"uid={uid}, pct={pct}, cnt={cnt}")
            for _ in range(0, cnt):
                candidate_likeliness.append(uid)
        logging.debug(f"candidate likeliness count: {len(candidate_likeliness)}")
        #logging.debug(f"{candidate_likeliness}")
        sys.exit(0)
        return candidate_likeliness

    

    def _rank_party(self, party: str, party_cnt: int=1) -> tuple(float, int): 
        weight = 40

        # If Democrat 48/100, Republican 48/100, Green 4/100, Constitution 1/100m 
        # Libertarian 2/100, Progressive 1/100m , Reform 0.5/100
        if party in ['Democrat', 'Republican']:
            points = ((48 + random.uniform(0, 0.9)) / party_cnt) 
        elif party == 'Green':
            points = ((4 + random.uniform(0, 0.9)) / party_cnt) 
        elif party == 'Libertarian':
            points = ((2 + random.uniform(0, 2)) /  party_cnt) 
        else:
            points = ((random.uniform(0.33, 1)) /  party_cnt)
        print(f"_rank_party(): points={points}, weight={weight}")
        return points, weight

    def _rank_duration(self, duration: int) -> tuple(float, int):  # 4pts 
        # Longer the duration the higher the contribution, media attention
        weight = 20
        pct = duration / ELECTION_DURATION

        return pct, weight

    def _rank_contributions(self, contributions: float) -> tuple(float, int): # 5pt
        weight = 25
        
        # Higher the more likely to pick
        pct = (contributions / self.total_contributions)

        return pct, weight
    
    def _rank_placement_on_ballot(self, uid: str) -> tuple(float, int): # 2pt
        weight = 10

        index = get_index_by_uid(self.candidates, uid)
        if index == 0:
            return 1, weight

        candidate_cnt = len(self.candidates)
        place = index + 1
        pct = (1 - (place / candidate_cnt))
    
        return pct, weight
        
    def _rank_name(self, name: str) -> int: # 1pt
        weight = 5

        # The longer the name the harder to pronounce the least likely to vote for that andidate
        if len(name) > self.mean_name_len:
            return 0, 1

        return 1, weight

    def _count_parties(self) -> dict:
        party_cnts = {}

        for party in POLITICAL_PARTIES:
            party_cnts[party] = 0

            for candidate in self.candidates:
                if candidate.party == party:
                    party_cnts[party] += 1
   
        return party_cnts
