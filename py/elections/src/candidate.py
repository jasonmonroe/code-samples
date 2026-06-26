# src/candidate.py

# Python Libraries
import logging
import random
from statistics import mean

# Local Libraries
from src.constants import (
    BALLOT_FRESH,
    CANDIDATE_DONATION_MAX, 
    CANDIDATE_DONATION_MIN, 
    CANDIDATE_NAME_POOL, 
    CANDIDATE_DEFAULT_COUNT, 
    DEFAULT_VOTER_COUNT, 
    ELECTION_DURATION, 
    POLITICAL_PARTIES
    )
from src.utils import gen_uuid


class Candidate:
    def __init__(self, add_noise: bool=False):
        self.add_noise = add_noise
        self.uid = gen_uuid(6)
        self.name = self._get_name()
        self.party = self._get_party()
        self.duration = self._get_duration()
        self.donations = self.campaign()
        self.is_winner = None # False = removed from pool, True = winner, None = still in pool
        self.votes = BALLOT_FRESH
        self.total = 0
        #self.points = 0
        #self.score = 0
        #self.sys_totals = 0 # system totals


    def _get_name(self) -> str:
        names = CANDIDATE_NAME_POOL
        first_names = names["first"]
        last_names = names["last"]

        return random.choice(first_names) + ' ' + random.choice(last_names)

    def _get_party(self) -> str:
        return random.choice(POLITICAL_PARTIES)
    
    # @TODO -defunct
    @staticmethod
    def get_names() -> tuple(list, list):
        """
        Get a list of first and last names for candidates.

        :return: object: A dictionary of first and last names.
        """

        return CANDIDATE_NAME_POOL["first"], CANDIDATE_NAME_POOL["last"]

    # @TODO -defunct
    @staticmethod
    def get_parties():
        """
        List of political parties.
        :return: list: A list of political parties.
        """

        return POLITICAL_PARTIES


    # @todo this is where ElectionSys.contribute() will be
    #def campaign(self):
    #    pass

    # Campaign!
    def campaign(self, donor_cnt: int=None) -> float:
        # Initial donations before campaign starts

        donors = random.randint(CANDIDATE_DEFAULT_COUNT, DEFAULT_VOTER_COUNT * 3) if donor_cnt is None else donor_cnt
    
        # determine party, then determine likelyness of party donations
        amount = 0.0
        for _ in range(0, donors):
            min_contr, max_contr = self._donation_limits()
            amount += random.uniform(min_contr, max_contr) 
            #print(f'amt={amt}')

        return round(amount, 2)

    def _get_duration(self) -> int:
        start = random.randint(1, 45)
        return random.randint(start, ELECTION_DURATION)

    def _donation_limits(self) -> tuple:
        min_value = CANDIDATE_DONATION_MIN 
        
        if self.party in ['Democrat', 'Republican']:
            min_value = 100
            max_value = CANDIDATE_DONATION_MAX
        elif self.party in ['Green', 'Libertarian']:
            max_value = CANDIDATE_DONATION_MAX / 2
        elif self.party in ['Progressive']:
            max_value = CANDIDATE_DONATION_MAX / 2.5
        else:
            max_value = CANDIDATE_DONATION_MAX / 4

        return min_value, max_value

    @staticmethod
    def mean_name_len() -> int:
        names = CANDIDATE_NAME_POOL
        first_names = names["first"]
        last_names = names["last"]

        name_lens = []
        for i in range(0, len(first_names)):
            for j in range(0, len(last_names)):
                name_lens.append(len(first_names[i] + ' ' + last_names[j]))
      
        return int(mean(name_lens))
                