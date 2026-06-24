# Election Class
import random
from helpers import uid, ridx, place_str, map_id_to_candidate_index, MIN_CANDIDATES, MAX_CANDIDATES, Candidate, \
    MIN_VOTERS, MAX_VOTERS, MAX_CHOICES, PERCENTILE, NO_VOTE_PCT_THRESHOLD, NO_VOTE_VAL, show_output, sort_candidates, \
    FIRST_CHOICE_INDEX
from datetime import date

class Election:
    def __init__(self):
        self.ballots = []
        self.candidates = []
        self.pool = []  # pool of candidates to vote on
        self.results = [] # Election results

    def election_day(self):
        """
        Run the election.
        """

        self.register()
        self.vote()
        self.show_banner()
        self.tally()

    def show_banner(self):
        """
        Display the election banner.

        :return:
        """

        print('\n----------------------------')
        print('-- E L E C T I O N  D A Y --')
        print('       ', date.today().strftime("%B %d, %Y"))
        print('----------------------------')
        #print('-', date.today().strftime("%B %d, %Y"))
        print('- Candidates:', len(self.candidates))
        print('- Voters:', len(self.ballots))
        print('----------------------------')

    @staticmethod
    def get_parties():
        """
        List of political parties.
        :return: list: A list of political parties.
        """

        return [
            'Constitution',
            'Democrat',
            'Green',
            'Libertarian',
            'No-Party Affiliation',
            'Progressive',
            'Reform',
            'Republican'
        ]

    @staticmethod
    def get_names():
        """
        Get a list of first and last names for candidates.

        :return: object: A dictionary of first and last names.
        """

        return {
            'first': [
                'Alexander',
                'Aïsha',
                'Amelia',
                'Anaïs',
                'Aries',
                'Ava',
                'Benjamin',
                'Charlotte',
                'Chloë',
                'Dmitri',
                'Elijah',
                'Elizabeth',
                'Emma',
                'Ella',
                'Fatima',
                'Harper',
                'Henry',
                'Isabella',
                'James',
                'Jürgen',
                'León',
                'Lars',
                'Liam',
                'Lucas',
                'Matthew',
                'Michael',
                'Mia',
                'Ming',
                'Noah',
                'Oliver',
                'Olga',
                'Omar',
                'Samuel',
                'Scarlett',
                'Sophia',
                'Sofia',
                'Thaddeus',
                'William',
                'Yuki',
                'Zhang'
            ],
            'last': [
                'Abdullah',
                'Anderson',
                'Ben-Ali',
                'Brown',
                'Clark',
                'Davis',
                'Dupont',
                'Dubois',
                'Fernández',
                'Garcia',
                'García',
                'Gonzalez',
                'Harris',
                'Hussein',
                'Hernandez',
                'Johnson',
                'Johansson',
                'Jackson',
                'King',
                'Lee',
                'Lewis',
                'Lopez',
                'Martin',
                'Martinez',
                'Miller',
                'Moore',
                'Ramírez',
                'Ramirez',
                'Rodriguez',
                'Schmidt',
                'Sanchez',
                'Sharma',
                'Silva',
                'Smith',
                'Taylor',
                'Thomas',
                'Thompson',
                'Takahashi',
                'Ivanov',
                'Walker',
                'Wilson',
                'Wright',
                'Young',
                'Zhang',
                'Zimmerman'
            ]
        }

    # Validate input.  We only accept integers or blank space that will generate a random value.
    @staticmethod
    def validate_input (message, str_flag=False):
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

    def register (self):
        """
        Secretary of State registers candidates for the election.

        :return: None
        """
        show_output = False
        if self.validate_input('\nShow output? (y/n) ', True) == 'y':
            #global show_output
            show_output = True

        candidate_cnt = self.validate_input(f'How many candidates ({MIN_CANDIDATES} to {MAX_CANDIDATES}) will register for the election?')

        if candidate_cnt == '':
            candidate_cnt = 4 #random.randint(MIN_CANDIDATES, MAX_CANDIDATES)

        else:
            # Set candidate count within range.
            if candidate_cnt < MIN_CANDIDATES:
                candidate_cnt = MIN_CANDIDATES

            if candidate_cnt > MAX_CANDIDATES:
                candidate_cnt = MAX_CANDIDATES

        print(f'There are {candidate_cnt} candidates for this election.')

        # Register candidates
        self.declare_candidacy(candidate_cnt)

    # Declare candidacy by registering name and party affiliation for the election.
    def declare_candidacy (self, candidate_cnt):
        """
        Register candidates for the election.

        :param int candidate_cnt: Number of candidates that are registered.

        :return: None
        """

        full_names = Election.get_names()

        print('\n------------------')
        print('--- Candidates ---')
        print('------------------')

        # Make sure each uid is unique
        for _ in range(0, candidate_cnt) :
            uid_str = uid()
            party = random.choice(Election.get_parties())
            full_name = random.choice(full_names['first']) + ' ' + random.choice(full_names['last'])
            print(f'{uid_str} - {full_name} - {party}')

            self.candidates.append(Candidate(uid_str, full_name, party))

        print('-------------------------------------')

    def get_voter_cnt(self):
        """
        Get the number of voters who registered for this election.

        :return: Int voter_cnt: The number of voters who registered for this election.
        """

        voter_cnt = self.validate_input('\nHow many voters are there?')

        if voter_cnt == '':
            voter_cnt = random.randint(MIN_VOTERS, MAX_VOTERS)  # should be MAX_VOTERS
        else:
            if voter_cnt < MIN_VOTERS:
                voter_cnt = MIN_VOTERS

            elif voter_cnt > MAX_VOTERS:
                voter_cnt = MAX_VOTERS

        print(f'{voter_cnt} voters will vote in this election.')

        return voter_cnt

    def vote (self):
        """
        Vote in the election.
        Gets the number of voters and allows them to vote for candidates.
        """

        # Prompt for voters
        voter_cnt = self.get_voter_cnt()

        # Create a ballot for voters to vote on.
        choice_cnt = min(MAX_CHOICES, len(self.candidates))

        print('\n--- Voting ---')
        for i in range (0, voter_cnt):
            self.reset_pool()
            self.ballots.append([])

            #if show_output == 'y':
                #print(f'\nNew Ballot {self.ballots[i]}')
                #print(f'Voter {i} is voting...')

            for _ in range (0, choice_cnt):
                candidate_chosen = self.mark_candidate()
                self.ballots[i].append(candidate_chosen)

                #if show_output is True:
                 #   p_str = place_str(j, 'p')
                 #   print(f'Voter {i} voted {p_str} for Candidate ID: {candidate_chosen}')

            # Display ballot for voter
            print(f'Voter {i} - Ballot: {self.ballots[i]}')

    def mark_candidate (self):
        """
        Mark a candidate on the ballot.
        There is a small chance that a voter does not want to vote for a candidate at all.
        """

        no_vote_odds = random.randint(0, PERCENTILE)

        # The odds are 10% that a voter does not choose a candidate otherwise vote
        if no_vote_odds >= NO_VOTE_PCT_THRESHOLD:
            return self.choose_candidate()

        else:
            return NO_VOTE_VAL

    def choose_candidate (self):
        """
        Chooses a candidate that has yet to be chosen.
        Note: We can expand this with more thorough logic in choosing a candidate.  For now, just pick at random.

        returns:
           int: The candidate id chosen.
        """

        return self.pool.pop(ridx(self.pool))

    def reset_pool (self):
        """
        Reset the pool of candidates for new voters to vote on.
        """

        self.pool = []
        for i in range (len(self.candidates)):
            self.pool.append(self.candidates[i].id)

    def tally(self):
        """
        Tally votes for each candidate based on the voter's choice.
        """

        for i in range (0, len(self.ballots)):
            for vote_choice in range (0, len(self.ballots[i])):
                voted_id = self.ballots[i][vote_choice]

                #if show_output is True:
                #    print(f'Ballot {i} choice {vote_choice} for candidate {voted_id}')

                # Update the corresponding place attribute based on vote_choice.
                if voted_id != NO_VOTE_VAL:
                    index = map_id_to_candidate_index(voted_id, self.candidates)
                    self.candidates[index].votes[vote_choice] += 1

                else:
                    if show_output is True:
                        p_str = place_str(vote_choice, 'p')
                        print(f'Warning: Voter {i} did not vote for {p_str}.')

        print('\n------- BALLOT TALLIES -------')
        for i in range (0, len(self.candidates)):
            print(f' Candidate {self.candidates[i].id} ', self.candidates[i].votes)

        print('------------------------------')

    def save_results(self, title, sorted_candidates):
        """
        Save the election results
        """

        self.results.append({'title': title, 'candidates': sorted_candidates})

    def show_results(self, title=''):
        """
        Output the election results.

        :return:
        """

        self.candidates = sort_candidates(self.candidates)

        # Only show the first result for a popular vote system.
        if title == 'popular':
            place = place_str(FIRST_CHOICE_INDEX, 'p')
            print(f'{place}: ({self.candidates[FIRST_CHOICE_INDEX].id}) {self.candidates[FIRST_CHOICE_INDEX].name} - {self.candidates[FIRST_CHOICE_INDEX].party} Party - Total: {self.candidates[FIRST_CHOICE_INDEX].total}')

        else:
            for i in range(0, len(self.candidates)):
                place = place_str(i, 'p')
                print(f'{place}: ({self.candidates[i].id}) {self.candidates[i].name} - {self.candidates[i].party} Party - Total: {self.candidates[i].total}')


    # Traverse through a list of candidates that participated in the election using the Alternative Voting System.
    def show_candidate_results(self, candidates, title):

        print(f'\n* {title} *')

        max_total = len(self.ballots)

        for i in range (len(candidates)):
            if candidates[i].is_winner is True:
                print(f'\n*** Winner: {candidates[i].name } ***')

            totals_pct = get_totals_pct(candidates[i], max_total)

            print(f'\n=== Candidates ({candidates[i].id}) ===')
            print(f'Name: {candidates[i].name}')
            print(f'{candidates[i].party} Party')
            print(f'Total/Points: {candidates[i].total} ({totals_pct}%)')
            print('--- Votes ---')

            for j in range (0, MAX_CHOICES):
                print(f'{place_str(j, "p")}: {candidates[i].votes[j]}')

    def show_results2(self, ces_c, weight_c, next_c):
        self.show_banner()
        self.show_candidate_results(ces_c, 'Candidate Elimination System')
        self.show_candidate_results(weight_c, 'Weighted Voting System')
        self.show_candidate_results(next_c, 'Next Choice Voting System')
        print('\n')
