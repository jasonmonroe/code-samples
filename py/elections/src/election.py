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
import json

# Local Libraries
from src.candidate import Candidate
from src.candidate_chooser import CandidateChooser
from src.candidate_pool import CandidatePool
from src.constants import (

    CANDIDATE_COUNT_MIN,
    CANDIDATE_DEFAULT_COUNT,
    I_INFO,
    I_SMILING,
    MAX_LINE_LEN, 
    VOTER_DEFAULT_COUNT,
    DONOR_COUNT_MAX,
    DONOR_COUNT_MIN,
    ELECTION_DURATION,
    FIRST_CHOICE,
    I_BALLOT,
    I_QUES, 
    CANDIDATE_COUNT_MAX, 
    MAX_CHOICES, 
    POLITICAL_PARTIES,
    VOTE_BLANK,
    VOTER_MAX_COUNT,
    VOTER_MIN_COUNT,
    WEIGHT_NOISE,
    )
from src.utils import (
    calc_pct_change,
    mute_logger,
    placement,
    show_banner
)
from src.voter import Voter


class ElectionSys:
    def __init__(self, add_noise: bool=False):
        self.add_noise = add_noise
        self.candidates = {} 
        self.party_counts = []
        self.total_donations = 0.0 
        self.voters = {} 
        self.election_at = datetime.now().strftime("%B %d, %Y")
        self.register_at = self._get_register_at()

        self._candidate_chooser = None
        self._pool = None

        self.show_election_banner()

    def register(self) -> None:
        q_candidate_cnt = self._query_candidate_count()

        # --- Register and declare candidacy
        self._declare_candidacy(q_candidate_cnt)

        # --- Register voters
        q_voters_cnt = self._query_voter_count()
        self._register_voters(q_voters_cnt)
        
        # --- 🚩 Turn off logs if participation is too high!
        if len(self.candidates) > 50 or len(self.voters) > 1000:
            mute_logger(len(self.candidates), len(self.voters))

    def _get_register_at(self) -> str:
        duration = ELECTION_DURATION
        if self.add_noise:
            noise_diff = int(ELECTION_DURATION * WEIGHT_NOISE)  # 15% of 365 is 54 days
            duration += random.randint(-noise_diff, noise_diff)       

        return (datetime.now() - timedelta(days=duration)).strftime("%B %d, %Y")

    def _declare_candidacy(self, candidate_cnt: int) -> None:
        subtitles = []
        total_donations = 0.0
        padding_len = 22

        subtitles.append(f"{'UID':<{6}} | {'NAME':<{padding_len}} | PARTY")
        subtitles.append(f"{"-" *  MAX_LINE_LEN}")

        # Special Case
        # If candidate count is 9 and noise flag is on
        use_unique_parties = self.add_noise and candidate_cnt == len(POLITICAL_PARTIES)

        if use_unique_parties:
            message = "🌟 Special case: All 9 political parties will be represented by a candidate. 🌟"
            print(message)
            logging.info(message)
            political_party_pool = POLITICAL_PARTIES.copy()

        for _ in range(candidate_cnt):
            candidate = Candidate(self.add_noise)
            
            # Override party with a unique one
            if use_unique_parties:
                candidate.party = random.choice(political_party_pool)
                political_party_pool.remove(candidate.party)

            subtitles.append(f"{candidate.uid} | {candidate.name:<{padding_len}} | {candidate.party}")

            # Tabulate candidates
            self.candidates[candidate.uid] = candidate
            total_donations += candidate.donations
    
        # Total candidate donations
        self.total_donations = total_donations

        # Count candidate's political party representation
        self.party_counts = self._count_parties()

        show_banner(f'CANDIDATES ({candidate_cnt})', subtitles)
        logging.info(f'There are {candidate_cnt} candidates running in this election.')

        self._show_candidate_info() 

    def _show_candidate_info(self):
        subtitles = []
        for uid, candidate in self.candidates.items():
            subtitles.append(f"{I_SMILING} {candidate.name}")
            subtitles.append(f"  {I_INFO}  UID: {uid}")
            subtitles.append(f"  {I_INFO}  Party: {candidate.party}")
            subtitles.append(f"  {I_INFO}  Duration: {candidate.duration} days")
            subtitles.append(f"  {I_INFO}  Donations: ${candidate.donations:.2f}")
            subtitles.append("")

        show_banner("Candidate Information".upper(), subtitles)
        
    def _register_voters(self, voter_cnt: int) -> None:
        for _ in range(voter_cnt):
            voter = Voter(self.register_at, self.add_noise)
    
            self.voters[voter.uid] = voter
             
    def _query_candidate_count(self) -> int:
        # Query number of candidates.
        query_candidates = f"\nHow many candidates ({CANDIDATE_COUNT_MIN} to {CANDIDATE_COUNT_MAX}) will register for this election{I_QUES} "
        q_candidate_cnt = self._validate_input(query_candidates)

        if q_candidate_cnt == "":
            q_candidate_cnt = random.randint(CANDIDATE_COUNT_MIN, CANDIDATE_COUNT_MAX)

        if q_candidate_cnt < CANDIDATE_COUNT_MIN:
            q_candidate_cnt = CANDIDATE_DEFAULT_COUNT

        if q_candidate_cnt > CANDIDATE_COUNT_MAX:
            q_candidate_cnt = CANDIDATE_COUNT_MAX

        return q_candidate_cnt

    def _query_voter_count(self) -> int:
        # Query number of voters.
        query_voters = f"\nHow many voters will participate in this election{I_QUES} "
        q_voters_cnt = self._validate_input(query_voters)

        if q_voters_cnt == "":
            q_voters_cnt = VOTER_DEFAULT_COUNT

        if q_voters_cnt < VOTER_MIN_COUNT:
            q_voters_cnt = VOTER_MIN_COUNT

        if q_voters_cnt > VOTER_MAX_COUNT:
            q_voters_cnt = VOTER_MAX_COUNT
        
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

            if user_input == '' or user_input is None:
                return user_input

            try:
                if str_flag:
                    return str(user_input).lower()
                else:
                    return int(user_input)
            except ValueError:
                print('Invalid input. Please enter an integer or press enter for a random value to be used.')

    def _count_parties(self) -> dict:
        party_counts = {}

        for party in POLITICAL_PARTIES:
            party_counts[party] = 0

            for _, candidate in self.candidates.items():
                if candidate.party == party:
                    party_counts[party] += 1
   
        return party_counts

    def campaign(self) -> None:
        # Donate to candidate (again)
        logging.info('🤝🏾 Candidates are campaigning and getting more donors 🤝🏾')

        total_donations = round(self.total_donations, 2)
        
        for _, candidate in self.candidates.items():
            donor_cnt = random.randint(DONOR_COUNT_MIN, DONOR_COUNT_MAX)
            amount = candidate.campaign(donor_cnt)
            candidate.donations += amount
            total_donations += amount
        
        # Add to total donations
        self.total_donations = total_donations
        pct_change = calc_pct_change(total_donations, self.total_donations)
        
        msg = f'Wow! Your total donations went from ${total_donations} (pre-election) to ${self.total_donations}.'
        msg += f'\nA {pct_change}% increase.'
        logging.info(msg)

    def _get_max_choice(self) -> int:
        return min(MAX_CHOICES, len(self.candidates))

    def vote(self) -> None:
        # Reset candidate pool before picking unique candidates
        show_banner('VOTERS', f'There are {len(self.voters)} registered voters for this election.\n Majority needed: {int((len(self.voters) // 2) + 1)}', True, True)
        
        logging.info('Voting...')

        self._pool = CandidatePool(self.candidates)
        self._candidate_chooser = CandidateChooser(
            self._pool.get(),
            self.total_donations,
            self.party_counts,
            self.add_noise,
            )
        
        # Every voter casts a ballot, # Every voter has up to 4 choices
        for idx, (uid, voter) in enumerate(self.voters.items()):
             
            # Reset candidate pool and candidate favorables before picking unique candidates
            self._pool.reset()
            self._candidate_chooser.reset_favorables()

            if not voter.voted:
                continue

            logging.info(f"\n=== {idx}: Voter {uid} is voting. ===")

            choice = FIRST_CHOICE
            max_choice = self._get_max_choice()
            while choice < max_choice:
                logging.debug(f"# --- Choice: {choice} --- #")
               
                # Store the latest pool of candidates and sync with the candidates favorables
                self._candidate_chooser.candidates = self._pool.get()
                self._candidate_chooser.sync_favorables()
             
                candidate_chosen = None

                # --- ✅ VOTE --- #
                candidate_chosen = voter.execute(self._candidate_chooser, choice)

                if candidate_chosen is None:
                    logging.warning(f"Voter {uid} did not choose a candidate for {placement(choice)}.")
                else:
                    self._pool.remove(candidate_chosen)

                choice += 1

            # End choice loop
            logging.info(f"--- Voter[{idx}]:{uid} Ballot: {voter.ballot} ---")
             
        logging.info("# --- End of election day.  Polls are now closed. --- #\n\n")

    def tally(self) -> None:
        logging.info(f"# --- {I_BALLOT} Tallying Ballots {I_BALLOT} --- #")
        
        no_vote_ctr = 0
        for _, (_, voter) in enumerate(self.voters.items()):
            for choice, ballot_choice in enumerate(voter.ballot):
                logging.debug(f"!!! ballot_choice={ballot_choice}")
                if ballot_choice == VOTE_BLANK:
                    no_vote_ctr += 1
                    continue

                if ballot_choice != VOTE_BLANK:
                    self.candidates[ballot_choice].votes[choice] += 1
        
        self.show_ballot_banner()

        if not self.add_noise and no_vote_ctr > 0:
            logging.warning(f"'🚩 Note: There were {no_vote_ctr} no votes.")

    def show_ballot_banner(self):
        vote_str_len = 22
        subtitles = []
        subtitles.append(f"{'VOTES':<{vote_str_len}} | Candidate")
        subtitles.append(f"{"-" *  MAX_LINE_LEN}")

        for _, candidate in self.candidates.items():
            subtitles.append(f"{str(candidate.votes):<{vote_str_len}} | "
            f"{candidate.uid} - ({candidate.party[0:3].upper()}) {candidate.name}")

        show_banner('BALLOT TALLIES', subtitles)

    def show_election_banner(self):
        year = datetime.strptime(self.register_at, "%B %d, %Y").year

        title = f"ELECTION SYSTEMS ({year})"
        logging.info(title)

        subtitles = [] 
        subtitles.append(f"Registration Day: {self.register_at}")
        subtitles.append(f"Election Day: {self.election_at}")

        show_banner(title, subtitles, True, True)
    