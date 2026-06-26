# src/election.py

"""
+----------------------------------------------------------------------------
| ELECTION
+----------------------------------------------------------------------------
| Data for elections.
| Electioneers can have candidates registered as well as voters.
+----------------------------------------------------------------------------
"""

# Python Libraries
import logging
import random
import sys

# Local Libraries
#from src import candidate
from src.candidate import Candidate
from src.candidate_chooser import CandidateChooser
from src.constants import (
    BLANK_BALLOT, 
    CANDIDATE_DEFAULT_COUNT, 
    DEFAULT_VOTER_COUNT,
    FIRST_CHOICE,
    I_QUES, 
    MAX_CANDIDATES, 
    MAX_CHOICES, 
    #MIN_CANDIDATES, 
    NO_CHOICE_PCT_THRESHOLD,
    NO_VOTE_PCT_THRESHOLD, 
    NO_VOTE_VAL,
    PERCENTILE
    )
from src.utils import (
    calc_pct_change,

    get_index_by_uid,
    placement,
    show_banner
)


class ElectionSys:
    def __init__(self, add_noise: bool=False):
        self.add_noise = add_noise
        self.ballots = []
        self.candidates = []
        self.candidate_pool = []  # pool of candidates to vote on
        self.results = [] # Election results
        self.total_contributions = 0.0
        self.vote_selector = None

    def register(self) -> int:
        # @todo - uncomment q_candidate_cnt = self._query_candidate_count()
        q_candidate_cnt = 4

        # Declare candidacy
        self._declare_candidacy(q_candidate_cnt)
        return 14
        # @todo - uncomment return self._query_voter_count()

    def _sum_contributions(self) -> float:
        sum_val = 0
        for i in range(0, len(self.candidates)):
            sum_val += self.candidates[i].contributions

        return round(sum_val, 2)

    def _query_candidate_count(self) -> int:
        # Query number of candidates.
        query_candidates = f"\nHow many candidates ({CANDIDATE_DEFAULT_COUNT} to {MAX_CANDIDATES}) will register for this election{I_QUES} "
        q_candidate_cnt = self._validate_input(query_candidates)

        if q_candidate_cnt == '':
            q_candidate_cnt = random.randint(CANDIDATE_DEFAULT_COUNT, (CANDIDATE_DEFAULT_COUNT * 4))

        if q_candidate_cnt < CANDIDATE_DEFAULT_COUNT:
            q_candidate_cnt = CANDIDATE_DEFAULT_COUNT

        return q_candidate_cnt

    def _declare_candidacy(self, candidate_cnt: int) -> None:
        subtitles = []
        for _ in range(0, candidate_cnt):
            candidate = Candidate(self.add_noise)
            subtitles.append(f"Candidate: {candidate.uid} | {candidate.name} | Party: {candidate.party}")

            # Tabulate candidates
            self.candidates.append(candidate)
      
        # Total candidate contributions
        self.total_contributions = self._sum_contributions()

        show_banner(f'CANDIDATES ({candidate_cnt})', subtitles)
        logging.info(f'There are {candidate_cnt} candidates running in this election.')

    def _query_voter_count(self) -> int:
        # Query number of voters.
        query_voters = f"\nHow many voters will participate in this election{I_QUES} "
        q_voters_cnt = self._validate_input(query_voters)

        if q_voters_cnt == '':
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

    def reset_candidate_pool(self) -> None:
        logging.debug('Resetting candidate pool.') 

        pool = []
        for i in range(0, len(self.candidates)):
            pool.append(self.candidates[i])

        self.candidate_pool = pool

    def contribute(self, votor_cnt: int):
        # Donate to candidate
        logging.info('🤝🏾 Getting more campaign contributions 🤝🏾')
        total_contributions = self.total_contributions
        
        for i in range(0, len(self.candidates)):
            amt = self.candidates[i].get_contributions(votor_cnt)
            self.candidates[i].contributions += amt
        
        # Add to total contributions
        self.total_contributions = self._sum_contributions()
        pct_change = calc_pct_change(total_contributions, self.total_contributions)
        msg = f'Wow! Your total contributions went from ${total_contributions} (pre-election) to ${self.total_contributions}.'
        msg += f'\nA {pct_change}% increase.'

        logging.info(msg)

    def vote(self, voter_cnt: int=FIRST_CHOICE) -> None:
        if voter_cnt == 0:
            voter_cnt = self._query_voter_count()

        # Reset candidate pool before picking unique candidates
        self.reset_candidate_pool()
        
        self.vote_selector = CandidateChooser(
            self.candidate_pool,
            self.total_contributions,
            Candidate.mean_name_len(),
            self.add_noise,
            )

        show_banner('VOTERS', f'There are {voter_cnt} registered voters for this election.', True, True)
        
        logging.info('Voting...')

        choice_cnt = min(MAX_CHOICES, len(self.candidates))

        # Every voter casts a ballot, # Every voter has up to 4 choices
        for idx in range(voter_cnt):
            logging.info(f"voter {idx} is voting...")
            self.ballots.append([])

            # Reset candidate pool before picking unique candidates
            self.reset_candidate_pool()
            self.vote_selector.reset_likeliness()

            if self.add_noise:
                no_vote_odds = random.randint(0, PERCENTILE)
                if no_vote_odds < NO_VOTE_PCT_THRESHOLD:
                    logging.warning(f"Voter {voter_cnt} did not cast a ballot.")
                    self.ballots[idx] = BLANK_BALLOT
                    continue
            
            logging.debug(f"BEFORE pool len: {len(self.candidate_pool)}")

            choice = FIRST_CHOICE
            while choice < choice_cnt:
                logging.debug(f"\n\n# --- Choice: {choice} --- #")
                self.__output_pool()

                candidate_chosen = self._candidate_chooser()
                msg = f"Candidate chosen: {candidate_chosen}"
                logging.debug(msg)
        
                self.ballots[idx].append(candidate_chosen)  

                # Remove chosen candidate from pool
                candidate_idx = get_index_by_uid(self.candidate_pool, candidate_chosen)
                logging.debug(f"pop candidate_idx={candidate_idx}, uid={candidate_chosen} from pool.")
                if candidate_idx is not None:
                    self.candidate_pool.pop(candidate_idx)
                else:
                    logging.warning("Candidate index was not found! Moving onto next.")
                choice += 1

            logging.debug(f"Vote {idx} of {voter_cnt} casted.")

    def __output_pool(self):
        logging.debug(f"# --- Candidate Pool ({len(self.candidate_pool)})--- #")
        for idx, candidate in enumerate(self.candidate_pool):
            logging.debug(f"candidate = {vars(candidate)}")

    def _candidate_chooser(self) -> str:
        # Add some noise to the voting experience for realism.
        # The odds of a voter doesn't vote for a candidate by choice is no more than 1%.
        if self.add_noise:
            random_choice_odds = random.randint(0, PERCENTILE)
            if random_choice_odds <= NO_CHOICE_PCT_THRESHOLD:
                return NO_VOTE_VAL

        return self.vote_selector.pick(self.candidate_pool)

    def tally(self) -> None:
        logging.info("# --- Tallying ballots --- #")
        # This counts all the votes per candidate by each choice
        for i in range(0, len(self.ballots)):
            for vote_choice in range(0, len(self.ballots[i])): # always 4 
                voted_candidate_uid = self.ballots[i][vote_choice]
             
                if voted_candidate_uid != NO_VOTE_VAL: 
                    index = get_index_by_uid(self.candidates, voted_candidate_uid)
                    self.candidates[index].votes[vote_choice] += 1
                else:
                    logging.warning(f" Ballot{i} did not have a vote for {placement(vote_choice, 'p')}.")

        subtitles = []
        subtitles.append("     VOTES    | Candidate")
        for i in range(0, len(self.candidates)):
            subtitles.append(f"{self.candidates[i].votes}  | {self.candidates[i].uid} - ({self.candidates[i].party[0:3].upper()}) {self.candidates[i].name}")

        show_banner('BALLOT TALLIES', subtitles)
