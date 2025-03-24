"""
|--------------------------------------------------------------------------
| Voting System
|--------------------------------------------------------------------------
| This is the base class for voting systems.
| It contains the common methods
| and attributes that are shared among the voting systems.
"""

# Import Libraries
from helpers import show_output, MAX_CHOICES, NO_VOTE_VAL, FIRST_CHOICE_INDEX, map_id_to_candidate_index, sort_candidates

class VotingSystem:
    """
    Base class for voting systems.

    Attributes:
        title (str): The title of the voting system.
        candidates (list): A list of candidates in the election.
        ballots (list): A list of ballots cast in the election.
        winner_id (int): The ID of the winning candidate.
        majority (int): The majority vote needed to win the election.
        voter_cnt (int): The number of voters in the election.
        choice_vals (list): Weighted choice values for each place.
    """

    def __init__(self, candidates, ballots):
        self.title = ''
        self.candidates = candidates
        self.ballots = ballots
        self.winner_id = None
        self.voter_cnt = len(ballots)
        self.majority = round(self.voter_cnt / 2)
        self.choice_vals = []

    def show_banner(self):
        """
        Show the banner for the voting system.
        """

        title_val = f'\n- {self.title.upper()} VOTING SYSTEM -'
        title_len = len(title_val)

        print(title_val)
        print('-' * title_len)

    @staticmethod
    def declare_winner(name):
        """
        Output the winner of the election.
        """

        print('\n----- WINNER -----')
        print('', name)
        print('------------------')

    def determine_loser(self):
        """
        Determine the candidate with the fewest votes.
        If there is a tie, break the tie by comparing the next place voted for count.

        :return:
            Candidate: The candidate with the fewest votes
        """

        # Get the candidate with the fewest votes.
        pool_of_candidates = self.get_pool_of_candidates()

        if show_output is True:
            print('Pool of candidates left:', len(pool_of_candidates))

        # If there is only one candidate left, declare them the winner by technicality.
        if len(pool_of_candidates) == 1:
            winning_candidate = pool_of_candidates[FIRST_CHOICE_INDEX]
            winning_candidate.is_winner = True
            self.winner_id = winning_candidate.id

            print('Only one candidate left:', winning_candidate.id)
            print('No candidate has won a majority.  Declaring remaining candidate winner by technicality.')

            return None

        # Handle the case where multiple candidates have the same minimum points:
        # 1. Find the minimum total points.
        # 2. Identify all candidates with this minimum total.
        # 3. If there are multiple candidates with the same minimum points, break the tie by comparing the next place votes.
        # 4. The candidate with the fewest next place votes is the tie-breaker.
        min_votes_candidates = self.get_lowest_voted_candidate(pool_of_candidates, 'total')

        if len(min_votes_candidates) == 1:
            return min_votes_candidates[FIRST_CHOICE_INDEX]

        else:
            # We have multiple candidates that have the same number of votes.
            # Break the tie by looking at the next place voted for count.
            return self.break_tie(min_votes_candidates, 'min', FIRST_CHOICE_INDEX)


    def determine_winner_by_popular(self):
        """
        Determine the winner based on the highest total points.
        Determined by popularity

        :return: Candidates candidates: The list of candidates.
        """

        candidate = None
        candidates = self.get_highest_voted_candidate(self.candidates, 'total')

        if len(candidates) == 1:
            candidate = candidates[FIRST_CHOICE_INDEX]

        elif len(candidates) > 1:
            candidate = self.break_tie(candidates, 'max', FIRST_CHOICE_INDEX)

        if candidate is not None:
            self.declare_winner(candidate.name)

        else:
            print('* No winner found *')

        self.candidates = sort_candidates(self.candidates)

        return self.candidates

    def determine_winner_by_majority(self, round_num):
        """
        Determines winner by majority.
        Checks each candidate to see if they have the majority vote needed to win the election.

        Returns:
        bool: True if a candidate has the majority vote, False otherwise.
        """

        #print('Majority to win: ', self.majority)
        print('Round #', round_num)
        for i in range (0, len(self.candidates)):

            # Output results.
            print('Debug: Candidate:', self.candidates[i].id, 'Total:', self.candidates[i].total)

            if self.candidates[i].total > self.majority:
                self.candidates[i].is_winner = True
                self.winner_id = self.candidates[i].id

                self.declare_winner(self.candidates[i].name)
                return True

        print('* No winner found *\n')
        return False

    @staticmethod
    def get_highest_voted_candidate(candidates, data_type, choice=None):
        """
        Get the candidate with the highest number of votes.

        :param list candidates: A list of candidates to compare.
        :param string data_type: The data to compare.
        :param int choice: The choice to compare (optional)

        Returns:
           list: A list of candidates with the highest total points.
        """

        if data_type == 'total':
            return [max(candidates, key=lambda c: c.total)]
        else:
            return [max(candidates, key=lambda c: c.votes[choice])]

    @staticmethod
    def get_lowest_voted_candidate(candidates, data_type, choice=None):
        """
        Get the candidate with the lowest number of votes.

        :param list candidates: A list of candidates to compare.
        :param string data_type: The data type to compare.
        :param int choice: The choice to compare (optional)

        Returns:
           list: A list of candidates with the lowest total points.
        """

        if data_type == 'total':
            return [min(candidates, key=lambda c: c.total)]
        else:
            return [min(candidates, key=lambda c: c.votes[choice])]

    def remove_loser_from_ballot(self, loser):
        """
        Remove the losing candidate from the ballot.

        :param loser:
            Candidate: The losing candidate.

        :return:
        """

        for i in range (0, len(self.ballots)):
            for j in range(len(self.ballots[i]) - 1, -1, -1):
                if self.ballots[i][j] == loser.id:
                    self.ballots[i].pop(j) # Remove candidate from contention

    def get_pool_of_candidates(self):
        """
        Get the pool of candidates that are still in contention.
        
        :returns: 
            list: A list of candidates that are still in contention.
        """

        return [candidate for candidate in self.candidates if candidate.is_winner is None]

    def reset_candidate_totals(self):
        """
        Reset the total points for each candidate so we can count the first choice each round.
        """

        for candidate in self.candidates:
            candidate.total = 0

    def break_tie(self, candidates, mode, choice):
        """
        Break the tie by comparing the next choice voted for count.
        Note: We can break a tie with the highest or lowest total points.

        :param candidates candidates: List or candidates to compare.
        :param string mode: Declaring highest or lowest total points to aggregate.
        :param int choice: Choice order to break the tie.

        :return: candidate: candidate with the highest/lowest votes.
        """

        choice += 1

        if choice < MAX_CHOICES:
            while len(candidates) > 1 and choice < MAX_CHOICES:

                if mode == 'min':
                    candidates = self.get_lowest_voted_candidate(candidates, 'votes', choice)

                elif mode == 'max':
                    candidates = self.get_highest_voted_candidate(candidates, 'votes', choice)

                # If there are still multiple candidates with the same number of votes, break the tie again.
                candidates = self.break_tie(candidates, mode, choice)

            # Finally, only one candidate left.
            if len(candidates) == 1:
                return candidates[FIRST_CHOICE_INDEX]

            print('Warning: No clear winner.')
            return None

        else:
            print('Warning: Out of choices and still no clear winner.')
            return None

    # Used in Weighted System
    def break_tie_weighted(self, tied_candidates, choice):
        """
        Break the tie by comparing the next choice voted for count.
        Note: We can break a tie with the highest or lowest total points.

        :param [] tied_candidates:  List or candidates to compare.
        :param int choice: Choice Number

        :return: Int winner_id: The candidate with the highest/lowest votes.
        """
        if show_output is True:
            print('Breaking weighted tie...')

        winner_id = None
        tie_breaker_total = 0
        next_tied_candidates = []

        # If there is a tie in total points break the tie with whom got the most first place votes.
        for i in range (0, len(tied_candidates)):
            candidate = tied_candidates[i]
            total = 0

            for j in range (0, len(self.choice_vals)):
                total += candidate.votes[j] * self.choice_vals[j]
                candidate.total += total

                if total > tie_breaker_total:
                    tie_breaker_total = total
                    winner_id = candidate.id

                elif total == tie_breaker_total:
                    next_tied_candidates.append(candidate)

        # Recursion
        if len(next_tied_candidates) > 0:

            # Update the place value (started at 1st) and break the tie again.
            next_choice = choice + 1

            if next_choice < MAX_CHOICES:
                winner_id = self.break_tie_weighted(next_tied_candidates, next_choice)

        return winner_id
