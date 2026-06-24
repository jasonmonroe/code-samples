# src/choose_candidate.py

# Python Libraries
import logging
import random
import sys

# Local Libraries
from src.constants import CANDIDATE_LIKELYNESS_PICK_ODDS, ELECTION_DURATION, POLITICAL_PARTIES
from src.utils import get_candidate_by_uid, get_index_by_uid

class ChooseCandidate:
    def __init__(self, candidates: list, 
    #pool: list, 
    total_contributions: float, mean_name_len: int):
        
        self.candidates = candidates
        #self.pool = pool
        self.total_contributions = round(total_contributions, 2)
        self.mean_name_len = mean_name_len
        #self.likeliness = []
        self.max_score = 20
        self.party_counts = self._count_parties()

        # Build likeliness once at the beginning to get the odds.
        self.likeliness = self.get_likeliness()
        #random.shuffle(self.likeliness)
        #print(f"likeliness={self.likeliness}")
        #sys.exit(0)
  
    def pick(self) -> str:
        # Logic to pick candidate from candidate pool
        # Pick the likeliness that a voter will just pick a random candidate out of fatigue or a lack of information
        # Then pick a random number.  If that number is less than the likelness pick a random candidate from the candidate pool.
        # Otherwise, use voter logic to determine who they're most likely to pick
        pick_random_candidate_likeliness = random.randint(0, CANDIDATE_LIKELYNESS_PICK_ODDS)
        random_pick = random.randint(0, 100)

        logging.debug(f'Random candidate likeliness: {pick_random_candidate_likeliness}, random_pick:{random_pick}')

        if random_pick <= pick_random_candidate_likeliness:
            #print('\tPicking random candidate')
            logging.info('Picking random candidate...')
            random_candidate = random.choice(self.candidates)
            return random_candidate.uid

        # Either pick max score OR create a list of 100 with number of indices based on the score, the higher the score the candidaete, the higher
        # the representation of indices.  Then pick a random number
        #likeness_list = self.get_likeliness()
        #print('Picking candidate by logic...')
        logging.info('Picking candidate by logic...')
        return random.choice(self.likeliness)

        # Note: For now just randomly pick one
        

    # Logic to pick a candidate
    """
    Logic to pick a candidate.  Party, Gender name, placement on the ballot, campaign contributions, duration of candidacy
    """

    def _calc_likeliness(self) -> dict:
        likeliness = []
        #pct_sum = 0

        #for uid in self.pool:
        #for uid in self.candidates:
        for candidate in self.candidates:
            #candidate = get_candidate_by_uid(self.candidates, uid)

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
            likeliness_scores["pct"] = (score / self.max_score)
            #pct_sum += likeliness_scores["pct"]
            
            #print(f'uid={uid}, likeliness_scores={likeliness_scores}')
            #print("\n")
            logging.debug(f'Score: {score}')
            likeliness.append({'uid': candidate.uid, 'score': score, 'pct': likeliness_scores["pct"]})

        #print(f'pct_sum={pct_sum}')

        return likeliness

        
    def _convert_to_list(self, likeliness: dict) -> list:
        candidate_likeliness = []
        #print(f'likeliness={likeliness}')
        for candidate in likeliness:
            #print(f'candidate={candidate}')
            uid = candidate["uid"]
            pct = candidate["pct"]
            cnt = int(pct * 1000)
            
            for _ in range(0, cnt):
                candidate_likeliness.append(uid)

        # shuffle list
        #random.shuffle(candidate_likeliness)
      
        return candidate_likeliness

    def get_likeliness(self) -> list:
        likeliness = self._calc_likeliness()
        #print(f'likeliness = {likeliness}')
        return self._convert_to_list(likeliness)


    def _rank_party(self, party: str, party_cnt: int=1) -> tuple(float, int): # 8 pts
        weight = 8

        # If Democrat 48/100, Republican 48/100, Green 4/100, Constitution 1/100m Libertarian 2/100, Progressive 1/100m , Reform 0.5/100
        if party in ['Democrat', 'Republican']:
            points = (((48 + random.uniform(0, 0.9)) / party_cnt) / 100)
        elif party == 'Green':
            points = (((4 + random.uniform(0, 0.9)) / party_cnt) / 100) 
        elif party == 'Libertarian':
            points = (((2 + random.uniform(0, 2)) /  party_cnt) / 100) 
        else:
            points = (((random.uniform(0.33, 1)) /  party_cnt) / 100) 
        #print(f'party = {party}, points = {points}')
        return points, weight
         
    def _rank_duration(self, duration: int) -> tuple(float, int):  # 4pts # Longer the duration the higher the contribution, media attention
        weight = 4
        #print(f'(({duration} / ELECTION_DURATION)) = {(duration / ELECTION_DURATION)}')
        pct = duration / ELECTION_DURATION
        #print(f'pct = {pct}')
        return pct, weight

    def _rank_contributions(self, contributions: float) -> tuple(float, int): # 5pt
        weight = 5
        #print(f'({contributions} / self.total_contributions) ={(contributions / self.total_contributions) }')
        
        # Higher the more likely to pick
        pct = (contributions / self.total_contributions)
        #print(f'pct = {pct}')
        return pct, weight
    
    def _rank_placement_on_ballot(self, uid: str) -> tuple(float, int): # 2pt
        weight = 2

        index = get_index_by_uid(self.candidates, uid)
        if index == 0:
            return 1, weight

        candidate_cnt = len(self.candidates)
        place = index + 1
        # 1/5=100-20=80 2/5=100-40, 3/5 =100-60=40, 4/5=100-80, 5/5=100-100
        #print(f'index_rank={place}, candidate_cnt= {candidate_cnt}')
        #ct =  ((100 - ((index + 1) / candidate_cnt)) / 100 )
        pct = (1 - (place / candidate_cnt))
        #print(f'pct={pct}')
        return pct, weight
        

    def _rank_name(self, name: str) -> int: # 1pt
        weight = 1

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
            #for uid in self.pool:
            #for uid in self.candidates:
            #    candidate = get_candidate_by_uid(self.candidates, uid)
            #    if candidate.party == party:
            #            party_cnts[party] += 1

        return party_cnts
