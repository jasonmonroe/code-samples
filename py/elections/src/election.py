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
from datetime import datetime, timedelta
import logging
import random
import sys

# Local Libraries
#from src import candidate
from src import candidate
from src.candidate import Candidate
from src.candidate_chooser import CandidateChooser
from src.candidate_pool import CandidatePool
from src.constants import (
    BALLOT_BLANK, 
    CANDIDATE_DEFAULT_COUNT, 
    DEFAULT_VOTER_COUNT,
    DONOR_COUNT_MAX,
    DONOR_COUNT_MIN,
    ELECTION_DURATION,
    FIRST_CHOICE,
    I_BALLOT,
    I_QUES, 
    CANDIDATE_COUNT_MAX, 
    MAX_CHOICES, 
    CANDIDATE_COUNT_MIN, 
    NO_CHOICE_PCT_THRESHOLD,
    POLITICAL_PARTIES,
    VOTE_BLANK_PCT_THRESH, 
    VOTE_BLANK,
    PERCENTILE
    )
from src.utils import (
    calc_pct_change,

    get_index_by_uid,
    placement,
    show_banner
)
from src.voter import Voter

# @TODO rename donations to donations
class ElectionSys:
    def __init__(self, add_noise: bool=False):
        self.add_noise = add_noise
        self.voters = []
        self.ballots = [] #@todo - defunct
        self.candidates = []
        self.candidate_pool = []  # pool of candidates to vote on
        self.results = [] # Election results
        self.total_donations = 0.0
        self.party_counts = []
        self.election_at = datetime.now().strftime("%B %d, %Y")
        self.register_at = self._get_register_at()

        self._candidate_chooser = None
        self._pool = CandidatePool(self.candidates)

        #self.voter = Voter()

    def register(self) -> bool:
        # @TODO - uncomment q_candidate_cnt = self._query_candidate_count()
        q_candidate_cnt = 4

        # Declare candidacy
        self._declare_candidacy(q_candidate_cnt)

        # Register voters
        
        # @TODO - uncomment q_voters_cnt = self._query_voter_count()
        q_voters_cnt = 14

        for _ in range(0, q_voters_cnt):
            self.voters.append(Voter(self.register_at, self.add_noise))

        # --- 🚩 Turn off logs if participation is too high!
        if len(self.candidates) > 50 or len(self.voters) > 1000:
            return True
        
        return False


    def _get_register_at(self) -> str:
        duration = ELECTION_DURATION
        if self.add_noise:
            noise_diff = int(ELECTION_DURATION * 0.15)  # 15% of 365 is 54 days
            duration += random.randint(-noise_diff, noise_diff)       

        return (datetime.now() - timedelta(days=duration)).strftime("%B %d, %Y")

    def _declare_candidacy(self, candidate_cnt: int) -> None:
        subtitles = []
        for _ in range(0, candidate_cnt):
            candidate = Candidate(self.add_noise)
            subtitles.append(f"Candidate: {candidate.uid} | {candidate.name} | Party: {candidate.party}")

            # Tabulate candidates
            self.candidates.append(candidate)
      
        # Total candidate donations
        self.total_donations = self._sum_donations()

        # Count candidate's political party representation
        self.party_counts = self._count_parties()

        show_banner(f'CANDIDATES ({candidate_cnt})', subtitles)
        logging.info(f'There are {candidate_cnt} candidates running in this election.')
        
    def _query_candidate_count(self) -> int:
        # Query number of candidates.
        query_candidates = f"\nHow many candidates ({CANDIDATE_DEFAULT_COUNT} to {CANDIDATE_COUNT_MAX}) will register for this election{I_QUES} "
        q_candidate_cnt = self._validate_input(query_candidates)

        if q_candidate_cnt == '':
            q_candidate_cnt = random.randint(CANDIDATE_DEFAULT_COUNT, (CANDIDATE_DEFAULT_COUNT * 4))

        if q_candidate_cnt < CANDIDATE_DEFAULT_COUNT:
            q_candidate_cnt = CANDIDATE_DEFAULT_COUNT

        return q_candidate_cnt

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

    def campaign(self) -> None:
        # Donate to candidate (again)
        logging.info('🤝🏾 Candidates are campaigning and getting more donors 🤝🏾')

        total_donations = self.total_donations
        donor_cnt = random.randint(DONOR_COUNT_MIN, DONOR_COUNT_MAX)
        
        for i in range(0, len(self.candidates)):
            amt = self.candidates[i].campaign(donor_cnt)
            self.candidates[i].donations += amt
        
        # Add to total donations
        self.total_donations = self._sum_donations()
        pct_change = calc_pct_change(total_donations, self.total_donations)
        msg = f'Wow! Your total donations went from ${total_donations} (pre-election) to ${self.total_donations}.'
        msg += f'\nA {pct_change}% increase.'

        logging.info(msg)

    def _sum_donations(self) -> float:
        sum_val = 0
        for i in range(0, len(self.candidates)):
            sum_val += self.candidates[i].donations

        return round(sum_val, 2)

    def vote(self) -> None:
        # Reset candidate pool before picking unique candidates
        self.reset_candidate_pool()

        self._candidate_chooser = CandidateChooser(
            self.candidate_pool,
            self.total_donations,
            self.party_counts,
            Candidate.mean_name_len(),
            self.add_noise,
            )

        voter_cnt = len(self.voters)

        show_banner('VOTERS', f'There are {voter_cnt} registered voters for this election.', True, True)
        
        logging.info('Voting...')

        choice_cnt = min(MAX_CHOICES, len(self.candidates))

        # Every voter casts a ballot, # Every voter has up to 4 choices
        for idx, voter in enumerate(self.voters):
            

            # Reset candidate pool and candidate likeliness before picking unique candidates
            self.reset_candidate_pool()
            self._candidate_chooser.reset_likeliness()

            self.ballots.append([]) # Ignore

            if not voter.voted:
                self.ballots[idx] = BALLOT_BLANK # Ignore
                continue

            logging.debug(f"BEFORE pool len: {len(self.candidate_pool)}")

            logging.info(f"{idx}: Voter {voter.uid} is voting...")

            choice = FIRST_CHOICE
            while choice < choice_cnt:
                logging.debug(f"\n\n# --- Choice: {choice} --- #")
                self._show_pool()

                # Update class with current candidate pool
                ##logging.debug("Refreshing candidate_chooser.candidates from pool...")

                #logging.debug("DBG: BEFORE self._candidate_chooser.candidates refresh")
                #for candidate_chooser_candidate in self._candidate_chooser.candidates:
                #    logging.debug(f"chooser.candidate = {vars(candidate_chooser_candidate)}")
                
                #self._candidate_chooser.candidates = self.candidate_pool
                #logging.debug(f"DBG: REFRESHED self._candidate_chooser.candidates!")
                
                #logging.debug("DBG: AFTER self._candidate_chooser.candidates refresh")
                #for candidate_chooser_candidate in self._candidate_chooser.candidates:
                #    logging.debug(f"chooser.candidate = {vars(candidate_chooser_candidate)}")
                

                #candidate_chosen = self._candidate_chooser.decision()
                candidate_chosen = None

                # --- ✅ VOTE --- #
                candidate_chosen = voter.execute(self._candidate_chooser, choice)
                logging.debug(f"DBG! choice:{choice} voter[{idx}].ballot[{choice}] = {voter.ballot[choice]}")

                logging.debug("Checking candidate pool manually")
                for candidate in self.candidate_pool:
                    logging.debug(f"candidate = {vars(candidate)}")

                logging.debug("Checking candidate   manually")
                for candidate in self.candidates:
                    logging.debug(f"candidate = {vars(candidate)}")
                
                #self.ballots[idx].append(candidate_chosen)  # Ignore
                
                if candidate_chosen is None:
                    logging.warning(f"Voter {voter.uid} did not choose a candidate for {placement(choice)}.")
                else:
                    self.remove_candidate_from_pool(candidate_chosen)

                choice += 1
                
            logging.debug(f"Vote {idx} of {voter_cnt} casted.")
            import json
            logging.debug(json.dumps([u.__dict__ for u in self.voters], indent=4))

    def tally(self) -> None:
        logging.info(f"\n# --- {I_BALLOT} Tallying ballots {I_BALLOT} --- #")
        
        for i, voter in enumerate(self.voters):
            logging.debug(f"{i} voter: {voter.uid}")
            for choice, ballot in enumerate(voter.ballot):
                logging.debug(f"choice: {choice} voted for: {ballot}")
                voter_candidate_uid = ballot

                if voter_candidate_uid != VOTE_BLANK:
                    candidate_idx = get_index_by_uid(self.candidates, voter_candidate_uid)
                    #logging.error("Why is there an error?")
                    #logging.error(f"candidate_idx={candidate_idx}, choice={choice}, self.candidates[candidate_idx]={vars(self.candidates[candidate_idx])}")
                    self.candidates[candidate_idx].votes[choice] += 1
        
        self.show_ballot_banner(self.candidates)
                
    def show_ballot_banner(self, candidates):
        subtitles = []
        subtitles.append("     VOTES    | Candidate")
        for i in range(0, len(candidates)):
            subtitles.append(f"{candidates[i].votes}  | {candidates[i].uid} - ({candidates[i].party[0:3].upper()}) {candidates[i].name}")

        show_banner('BALLOT TALLIES', subtitles)

    
    

    def remove_candidate_from_pool(self, candidate_chosen):
        # Remove chosen candidate from pool
        logging.debug(f"remove_candidate_from_pool({candidate_chosen})")
        candidate_idx = get_index_by_uid(self.candidate_pool, candidate_chosen)
        #logging.debug(f"pop candidate_idx={candidate_idx}, uid={candidate_chosen} from pool.")
        logging.debug(f"Before removal lets view the current candidate pool")
        self._show_pool()
        if candidate_idx is not None:
            logging.debug(f"Removing candidate_idx: {candidate_idx}, candidate: {candidate_chosen} from pool!")
            self.candidate_pool.pop(candidate_idx)
        else:
            logging.warning("Candidate's index was not found! Moving onto the next.")
        logging.debug(f"After removal lets check the latest candidate pool!")
        self._show_pool()
    
    def reset_candidate_pool(self) -> None:
        logging.debug('Resetting candidate pool for new voter.') 
        
        pool = []
        for i in range(0, len(self.candidates)):
            logging.debug(f"CHECK: i: {i}, self.candidates[{i}]: {vars(self.candidates[i])}")
            pool.append(self.candidates[i])

        self.candidate_pool = pool

    # Helper function
    def _show_pool(self):
        logging.debug(f"# --- Candidate Pool ({len(self.candidate_pool)}) --- #")
        for idx, candidate in enumerate(self.candidate_pool):
            logging.debug(f"candidate[{idx}] = {vars(candidate)}")


    # @TODO 
    def vote_orig(self) -> None:
        if voter_cnt == 0:
            voter_cnt = self._query_voter_count()

        # Reset candidate pool before picking unique candidates
        self.reset_candidate_pool()

        mean_name_len = Candidate.mean_name_len(),
        
        self._candidate_chooser = CandidateChooser(
            self.candidate_pool,
            self.total_donations,
            self.party_counts,
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
            self._candidate_chooser.reset_likeliness()

            if self.add_noise:
                no_vote_odds = random.randint(0, PERCENTILE)
                if no_vote_odds < VOTE_BLANK_PCT_THRESH:
                    logging.warning(f"Voter {voter_cnt} did not cast a ballot.")
                    self.ballots[idx] = BALLOT_BLANK
                    continue
            
            logging.debug(f"BEFORE pool len: {len(self.candidate_pool)}")

            choice = FIRST_CHOICE
            while choice < choice_cnt:
                logging.debug(f"\n\n# --- Choice: {choice} --- #")
                self._show_pool()

                candidate_chosen = None

                # Update class with current candidate pool
                self._candidate_chooser.candidates = self.candidate_pool
                candidate_chosen = self._candidate_chooser.decision()

                # --- ✅ VOTE --- #
                self.ballots[idx].append(candidate_chosen)  

                self.remove_candidate_from_pool(candidate_chosen)

                choice += 1
                
                """
                # @TODO - ignore below this line
                

                candidate_chosen = self._candidate_chooser()
                msg = f"Candidate chosen: {candidate_chosen}"
                logging.debug(msg)


                # --- ✅ VOTE --- #
                self.ballots[idx].append(candidate_chosen)  

                # Remove chosen candidate from pool
                candidate_idx = get_index_by_uid(self.candidate_pool, candidate_chosen)
                logging.debug(f"pop candidate_idx={candidate_idx}, uid={candidate_chosen} from pool.")
                if candidate_idx is not None:
                    self.candidate_pool.pop(candidate_idx)
                else:
                    logging.warning("Candidate index was not found! Moving onto next.")
                """
                
            logging.debug(f"Vote {idx} of {voter_cnt} casted.")


    # @TODO - defunct
    def tally_orig(self) -> None:
        logging.info(f"# --- {I_BALLOT} Tallying ballots {I_BALLOT} --- #")
        # This counts all the votes per candidate by each choice
        for i in range(0, len(self.ballots)):
            for vote_choice in range(0, len(self.ballots[i])): # always 4 
                voted_candidate_uid = self.ballots[i][vote_choice]
             
                if voted_candidate_uid != VOTE_BLANK: 
                    index = get_index_by_uid(self.candidates, voted_candidate_uid)
                    self.candidates[index].votes[vote_choice] += 1
                else:
                    logging.warning(f" Ballot{i} did not have a vote for {placement(vote_choice, 'p')}.")

        subtitles = []
        subtitles.append("     VOTES    | Candidate")
        for i in range(0, len(self.candidates)):
            subtitles.append(f"{self.candidates[i].votes}  | {self.candidates[i].uid} - ({self.candidates[i].party[0:3].upper()}) {self.candidates[i].name}")

        show_banner('BALLOT TALLIES', subtitles)


    # @TODO - defunct
    def _count_parties(self) -> dict:
        party_counts = {}

        for party in POLITICAL_PARTIES:
            party_counts[party] = 0

            for candidate in self.candidates:
                if candidate.party == party:
                    party_counts[party] += 1
   
        return party_counts


    # @TODO - defunct
    def ___candidate_chooser(self) -> str:
        # Add some noise to the voting experience for realism.
        # The odds of a voter doesn't vote for a candidate by choice is no more than 1%.
        if self.add_noise:
            random_choice_odds = random.randint(0, PERCENTILE)
            if random_choice_odds <= NO_CHOICE_PCT_THRESHOLD:
                return VOTE_BLANK

        return self._candidate_chooser.decision(self.candidate_pool)
