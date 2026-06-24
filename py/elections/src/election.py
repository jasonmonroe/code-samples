# src/election.py

"""
+----------------------------------------------------------------------------
| ELECTION
+----------------------------------------------------------------------------
| Data for elections.
"""

# Python Libraries
import logging
import random
import sys

#from src import candidate
from src.candidate import Candidate
from src.choose_candidate import ChooseCandidate
from src.constants import BLANK_BALLOT, CANDIDATE_DEFAULT_COUNT, DEFAULT_VOTER_COUNT, MAX_CANDIDATES, MAX_CHOICES, MIN_CANDIDATES, NO_CHOICE_PCT_THRESHOLD, NO_VOTE_PCT_THRESHOLD, NO_VOTE_VAL
from src.utils import calc_pct_change, gen_uuid,   get_index_by_uid, placement, show_banner


class ElectionSys:
    def __init__(self, add_noise: bool=False):
        self.ballots = []
        self.candidates = []
        #self.candidate_pool = []  # pool of candidates to vote on
        self.results = [] # Election results
        self.add_noise = add_noise
        self.total_contributions = 0.0
        self.vote_selector = None
    

    def register(self) -> int:
       q_candidate_cnt = self._query_candidate_count()

       # Declare candidacy
       self._declare_candidacy(q_candidate_cnt)
       #self.reset_candidate_pool()

       return self._query_voter_count()

    def _sum_contributions(self) -> float:
        sum_val = 0
        for i in range(0, len(self.candidates)):
            sum_val += self.candidates[i].contributions

        return round(sum_val, 2)

    def _query_candidate_count(self) -> int:

        # Query number of candidates.
        query_candidates = f"\nHow many candidates ({MIN_CANDIDATES} to {MAX_CANDIDATES}) will register for this election? _"
        q_candidate_cnt = self._validate_input(query_candidates)

        if q_candidate_cnt == '':
            q_candidate_cnt = random.randint(CANDIDATE_DEFAULT_COUNT, (CANDIDATE_DEFAULT_COUNT * 4))

        if q_candidate_cnt < CANDIDATE_DEFAULT_COUNT:
            q_candidate_cnt = CANDIDATE_DEFAULT_COUNT

        return q_candidate_cnt

    def _declare_candidacy(self, candidate_cnt: int) -> None:

        #names = Candidate.get_names()
        #parties = Candidate.get_parties()

        subtitles = []
        for _ in range(0, candidate_cnt):
            #uid = gen_uuid(6)
            #party = random.choice(parties)
            #candidate_name = random.choice(names['first']) + ' ' + random.choice(names['last'])
            
            candidate = Candidate()
            print(f'DBG: candidate={candidate}')
            #subtitles.append(f"Candidate: {uid} | {candidate_name} | Party: {party}")
            subtitles.append(f"Candidate: {candidate.uid} | {candidate.name} | Party: {candidate.party}")

            # Tabulate candidates
            self.candidates.append(candidate)
            #self.candidates.append(Candidate(uid, candidate_name, party))

        # Total candidate contributions
        self.total_contributions = self._sum_contributions()

        show_banner(f'CANDIDATES ({candidate_cnt})', subtitles)
        logging.info(f'There are {candidate_cnt} candidates running in this election.')
        print(f'There are {candidate_cnt} candidates running in this election.')

    def _query_voter_count(self) -> int:
        # Query number of voters.
        query_voters = f"\nHow many voters will participate in this election? _"
        q_voters_cnt = self._validate_input(query_voters)

        if q_voters_cnt == '':
            #q_voters_cnt = random.randint(DEFAULT_VOTER_COUNT, (DEFAULT_VOTER_COUNT * 8))
            q_voters_cnt = random.randint(DEFAULT_VOTER_COUNT, 20)
        if q_voters_cnt < DEFAULT_VOTER_COUNT:
            q_voters_cnt = DEFAULT_VOTER_COUNT

        return q_voters_cnt

    def _validate_input(self, message: str, str_flag: bool=False) -> str | int:
        """
        Only accept integers or blank space that will generate a random value.

        :param string message: Message to display to the user.
        :param bool str_flag: Is the input a string or not?

        :returns: None

        :raises: ValueError: If the input is not an integer or string.
        """
        while True:
            user_input = input(message)

            if user_input == '':
                return user_input

            try:
                if str_flag:
                    return str(user_input).lower()
                else:
                    return int(user_input)
            except ValueError:
                print('Invalid input. Please enter an integer or press enter for a random value to be used.')

    # @todo - delete
    def reset_candidate_pool(self) -> None:
        logging.info('Resetting candidate pool.')

        pool = []
        for i in range(len(self.candidates)):
            pool.append(self.candidates[i].uid)

        self.candidate_pool = pool

    def contribute(self, votor_cnt: int):
        # Donate to candidate
        logging.info('Getting more campaign contributions...')
        total_contributions = self.total_contributions

        for i in range(0, len(self.candidates)):
            amt = self.candidates[i].get_contributions(votor_cnt)
            self.candidates[i].contributions += amt
        
        # Add to total contributions
        # Total candidate contributions
        self.total_contributions = self._sum_contributions()

        #@todo - update
        increase_pct = calc_pct_change(total_contributions, self.total_contributions)

        print(f'Wow, total contributions went from ${total_contributions} (pre-election) to ${self.total_contributions}. A {increase_pct}& increase.')


    def vote(self, voter_cnt: int=0) -> None:
        if voter_cnt == 0:
            voter_cnt = self._query_voter_count()

        choice_cnt = min(MAX_CHOICES, len(self.candidates))
        self.vote_selector = ChooseCandidate(
            self.candidates,
            #self.candidate_pool,
            self.total_contributions,
            Candidate.mean_name_len()
            )

        show_banner('VOTERS', f'There are {voter_cnt} registered voters for this election.', True, True)
        
        logging.info('Voting...')

        # Every voter casts a ballot, # Every voter has up to 4 choices
        for idx in range(0, voter_cnt):
            self.ballots.append([])

            if self.add_noise:
                no_vote_odds = random.randint(0, 100)
                if no_vote_odds < NO_VOTE_PCT_THRESHOLD:
                    logging.warning(f"Voter {voter_cnt} did not cast a ballot.")
                    print('continue...\n')
                    self.ballots[idx] = BLANK_BALLOT
                    continue

            for _ in range(0, choice_cnt):
                candidate_chosen = self._choose_candidate()
                logging.debug(f'Candidate chosen: {candidate_chosen},')
                #print(f"Candidate chosen: {candidate_chosen}")
             
                self.ballots[idx].append(candidate_chosen)     

    def _choose_candidate(self) -> str:

        # Add some noise to the voting experience for realism.
        # The odds of the candidate doesn't vote for a candidate by choice is no more than 1%.
        if self.add_noise:
            no_choice_odds = random.randint(0, 100)
            if no_choice_odds <= NO_CHOICE_PCT_THRESHOLD:
                return NO_VOTE_VAL

        #selector = ChooseCandidate(self.candidates, self.candidate_pool, self.total_contributions, mean_name_len)
        return self.vote_selector.pick()

    def tally(self) -> None:
        # This counts all the votes per candidate by each choice
        #print(self.ballots)
        #sys.exit(1)
        for i in range(0, len(self.ballots)):
            for vote_choice in range(0, len(self.ballots[i])): # always 4 
                voted_candidate_uid = self.ballots[i][vote_choice]
                print(f"voted for {voted_candidate_uid}")
                if voted_candidate_uid != NO_VOTE_VAL: 
                    index = get_index_by_uid(self.candidates, voted_candidate_uid)
                    print(f"index={index}")
                    self.candidates[index].votes[vote_choice] += 1
                else:
                    logging.warning(f" Ballot{i} did not have a vote for {placement(vote_choice, 'p')}.")

        subtitles = []
        subtitles.append("    VOTES    | Candidate")
        for i in range(0, len(self.candidates)):
            
            subtitles.append(f"{self.candidates[i].votes} | {self.candidates[i].uid} - {self.candidates[i].name}")
            #subtitles.append(f"Candidate: {self.candidates[i].uid} | {self.candidates[i].votes}")

        show_banner('BALLOT TALLIES', subtitles)







    
        
