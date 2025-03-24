"""
|--------------------------------------------------------------------------
| Election.py
|--------------------------------------------------------------------------
| Jason Monroe
| jason@jasonmonroe.com
| December 2, 2024
|--------------------------------------------------------------------------
| This script simulates ranked choice voting implemented by the voters of
| the great state of Alaska.  Voters approved a revamp of the election
| season where no longer is it who gets the most votes wins the election but
| now a rank-choice voting system that takes into account overall voter sentiment.
| There are two different systems that can be implemented:
|
| Alaska Version
| --------------
| Candidate Elimination System
|	1. Majority Vote earner
|		a. Single candidate
|			i. Candidate advances unopposed
|		b. Two are more candidates
|		    i. Count all first place votes to determine winner
|		    ii. If no winner, eliminate last place candidate
|           iii. Apply the next place votes of the eliminated candidate to the first
|                place of remaining candidates.   
|
| Alternative Version 
| -------------------
| Weighted Voting System
|	1. Primary Majority Vote earner
|		a. Single candidate
|			i. Candidate advances unopposed
|		b. Two are more candidates
|			i. Tally all votes
|			ii. Weigh the votes with ranked choice formula.  Highest points wins.
|       c. Tie-breaker
|           i. If there is a tie in total points break the tie with whom got the most next 
|               place votes starting with first.    
|	2. Voting system
|		a. Voter votes by ranked choice.
|			i. First place votes = 1
|			ii. 2nd place votes = 1/2
|			iii. 3rd place votes  = 1/4
|			iv. 4th place votes = 1/8
|		b. Tally the votes for each candidate
|		c. Determine the winner based on the highest points.
|
|  Next Choice System
|	1. Majority Vote earner
|       a. Single candidate
|           i. Candidate advances unopposed
|       b. Two are more candidates
|           i. Count all first place votes to determine winner
|           ii. If no winner, count every voter's next choice votes
|
| Sources:
| @link https://www.elections.alaska.gov/election-information/#PRIM
| @link https://www.sightline.org/2024/10/25/whats-different-in-alaska-since-election-laws-changed/
| @link https://www.sightline.org/2022/07/28/in-alaskas-special-election-a-bipartisan-mindset-makes-sense/
| @link https://www.youtube.com/watch?v=lLU3lbrxMBI
| @link https://www.youtube.com/watch?v=oHRPMJmzBBw
"""

## Import libraries
import random
import uuid
from datetime import date

## Helper functions
max_choices = 4
no_vote_val = ''
percentile = 100
show_output = False

# Register election data and vote
def register_candidates_and_ballots():
    election = Election()
    # election.register()
    election.register_auto()
    election.vote()
    election.tally()

    return election

# Input voter ID and return index of candidate.
def map_id_to_candidate_index (voted_id, candidates):
    for index in range (0, len(candidates)):
        if voted_id == candidates[index].id:
            return index

# Return string of placement
def place_str (place, mode):
    if mode == 'a':
        attrs = ['first', 'second', 'third', 'fourth']
    else:
        attrs = ['1st Place', '2nd Place', '3rd Place', '4th Place']

    return attrs[place]

# Shortener get random index
def ridx (var):
    return random.randint(0, len(var) - 1)

# Unique ID for candidate
def uid(length=4):
    return str(uuid.uuid4())[:length]

def sort_candidates (candidates):
    return sorted (candidates, key=lambda candidate: candidate.total, reverse=True)

def get_totals_pct (candidate, max_points):
    return round ((candidate.total / max_points) * percentile, 2)

# Create a candidate object
class Candidate:
    def __init__(self, u_id, name, party):
        self.id = u_id
        self.name = name
        self.party = party
        self.is_winner = None # False = removed from pool, True = winner, None = still in pool
        self.votes = [0, 0, 0, 0]
        self.total = 0

class Election:
    def __init__(self):
        self.ballots = []
        self.candidates = []
        self.pool = []  # pool of candidates to vote on

    def show_banner(self):
        print('\n##########################')
        print('# E L E C T I O N  D A Y #')
        print('##########################')
        print('#', date.today().strftime("%B %d, %Y"))
        print('# Candidates:', len(self.candidates))
        print('# Voters:', len(self.ballots))
        print('##########################\n')

    @staticmethod
    def get_parties():
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
        return {
            'first': [
                'Alexander',
                'Aïsha',
                'Amelia',
                'Anaïs',
                'Ananya',
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
                'Thiago',
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
                'Martin',
                'Martinez',
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
                'Petrova'
            ]
        }

    # Validate input.  We only accept integers or blank space that will generate a random value.
    @staticmethod
    def validate_input (message, str_flag=False):
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

    # @todo temp method
    def register_auto (self):
        candidate_cnt = 4
        self.declare_candidacy(candidate_cnt)

    # Secretary of State registers declared candidates for the primary election.
    def register (self):
        min_candidates = 1
        max_candidates = 32

        global show_output
        show_output = False
        if self.validate_input('\nShow output? (y/n) ', True) == 'y':
            show_output = True

        candidate_cnt = self.validate_input(f'How many candidates ({min_candidates} to {max_candidates}) will register for the primary? ')

        if candidate_cnt == '':
            candidate_cnt = random.randint(min_candidates, max_candidates)

        else:
            # Set candidate count within range.
            if candidate_cnt < min_candidates:
                candidate_cnt = min_candidates

            if candidate_cnt > max_candidates:
                candidate_cnt = max_candidates

        print(f'There are {candidate_cnt} candidates for this primary election.')

        # Register candidates
        self.declare_candidacy(candidate_cnt)

    # Declare candidacy by registering name party for the primary
    def declare_candidacy (self, candidate_cnt):
        full_names = Election.get_names()

        print('\nCandidates')
        for i in range(0, candidate_cnt) :
            party = random.choice(Election.get_parties())
            full_name = random.choice(full_names['first']) + ' ' + random.choice(full_names['last'])
            print(f'{i}, {full_name}, {party}')

            # Make sure each uid is unique
            self.candidates.append(Candidate(uid(), full_name, party))

    # Get the number of voters who registered for this election
    def get_voter_cnt(self):
        min_voters = 25
        max_voters = 168000000  # 168,000,000
        voter_cnt = self.validate_input('\nHow many voters are there? ')

        if voter_cnt == '':
            voter_cnt = random.randint(min_voters, 100)  # should be max_voters
        else:
            if voter_cnt < min_voters:
                voter_cnt = min_voters

            elif voter_cnt > max_voters:
                voter_cnt = max_voters

        print(f'{voter_cnt} voters will vote in this primary election.')

        return voter_cnt

    # Vote in the election.
    def vote (self):
        # Prompt for voters
        voter_cnt = self.get_voter_cnt()
        #voter_cnt = 10  # For testing purposes

        # Create a ballot for voters to vote on.
        choice_cnt = min(max_choices, len(self.candidates))

        print('\nVoting...')
        for i in range (0, voter_cnt):
            self.reset_pool()
            self.ballots.append([])

            if show_output == 'y':
                print(f'\nNew Ballot {self.ballots[i]}')
                print(f'Voter {i} is voting...')

            for j in range (0, choice_cnt):
                candidate_chosen = self.mark_candidate()
                self.ballots[i].append(candidate_chosen)

                if show_output is True:
                    p_str = place_str(j, 'p')
                    print(f'Voter {i} voted {p_str} for Candidate ID: {candidate_chosen}')

            # Display ballot for voter
            print(f'Voter {i} ballot: {self.ballots[i]}')

    # Mark candidate on ballot.
    def mark_candidate (self):

        # There's a small chance that a voter does not want to vote for a candidate at all.
        no_vote_pct_threshold = 3
        no_vote_odds = random.randint(0, percentile)

        # The odds are 10% that a voter does not choose a candidate otherwise vote
        if no_vote_odds <= no_vote_pct_threshold:
            return no_vote_val

        else:
            return self.choose_candidate()

    # Choose a candidate that has not been chosen before.
    # Note: We can expand this with more thorough logic in choosing a candidate.  For now just pick at random.
    def choose_candidate (self):
        return self.pool.pop(ridx(self.pool))

    # Reset the pool of candidates for new voters to vote on.
    # Note: Pool should not exceed the number of candidates.
    def reset_pool (self):
        self.pool = []
        for i in range (len(self.candidates)):
            self.pool.append(self.candidates[i].id)

    # Tally votes and store based on voter choice.
    def tally (self):
        print('\nTallying votes...')
        if show_output == 'y':
            print('\nTallying votes...')
            print(self.ballots)

        for i in range (0, len(self.ballots)):
            for vote_choice in range (0, len(self.ballots[i])):
                voted_id = self.ballots[i][vote_choice]

                if show_output is True:
                    print(f'Ballot {i} choice {vote_choice} for candidate {voted_id}')

                if voted_id != no_vote_val:
                    # Update the corresponding place attribute based on vote_choice
                    index = map_id_to_candidate_index(voted_id, self.candidates)
                    self.candidates[index].votes[vote_choice] += 1

                else:
                    if show_output is True:
                        p_str = place_str(vote_choice, 'p')
                        print(f'Warning: Voter {i} did not vote for {p_str}.')

        print('Votes tallied.')

        if show_output is True:
            for i in range (0, len(self.candidates)):
                print(f'Candidate {self.candidates[i].id} Total:{self.candidates[i].total} Votes:', self.candidates[i].votes)

    # Traverse through list of candidates that participated in the election using the Alternative Voting System.
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

            for j in range (0, max_choices):
                print(f'{place_str(j, "p")}: {candidates[i].votes[j]}')

    def show_results(self, ces_c, weight_c, next_c):
        self.show_banner()
        self.show_candidate_results(ces_c, 'Candidate Elimination System')
        self.show_candidate_results(weight_c, 'Weighted Voting System')
        self.show_candidate_results(next_c, 'Next Choice Voting System')
        print('\n')


# Parent Class for voting system
class VotingSystem:
    def __init__(self, candidates, ballots):
        self.candidates = candidates
        self.ballots = ballots
        self.winner_id = None
        self.majority = round(len(ballots) / 2) + 1

    def determine_loser(self):
        #print('Determining loser...')

        # Get the candidate with the fewest votes.
        pool_of_candidates = self.get_pool_of_candidates()
        global show_output
        if show_output is True:
            print('Pool of candidates left:', len(pool_of_candidates))

        # Handle the case where multiple candidates have the same minimum points:
        # 1. Find the minimum total points.
        # 2. Identify all candidates with this minimum total.
        # 3. If there are multiple candidates with the same minimum points, break the tie by comparing the next place votes.
        # 4. The candidate with the fewest next place votes is the tie-breaker.
        min_votes_candidates = self.get_candidate_with_lowest_total(pool_of_candidates)

        if len(min_votes_candidates) == 1:
            return min_votes_candidates[0]
        else:
            # We have multiple candidates that have the same number of votes.
            # Break the tie by looking at the next place voted for count.
            vote_choice = 0
            return self.tie_breaker(min_votes_candidates, vote_choice)

    # Note: This method used in CandidateEliminationSystem & NextChoiceSystem
    def determine_winner(self):
        #print('Determining winner...')
        #print('Majority to win: ', self.majority)

        for i in range (0, len(self.candidates)):
            #print('Candidate:', self.candidates[i].id, 'Total:', self.candidates[i].total)
            if self.candidates[i].total > self.majority:
                #print(f'Winner found! Candidate {self.candidates[i].id} ', self.candidates[i].name, 'Total:', self.candidates[i].total)
                self.candidates[i].is_winner = True
                self.winner_id = self.candidates[i].id

                return True
            else:
                print(f'Candidate {self.candidates[i].id} Total:{self.candidates[i].total} does not have majority.')

        print('No winner found.')
        return False

    # Tally votes based on Alaska system
    def get_candidate_with_lowest_total(self, candidates):
        min_total = min(candidate.total for candidate in candidates)
        return [candidate for candidate in candidates if candidate.total == min_total]

    def tie_breaker(self, candidates, choice):
        if show_output is True:
            print('Attempting to break tie...')

        next_choice = choice + 1
        min_votes = candidates[0].votes[next_choice] # Initialize min votes with first index
        min_candidate = candidates[0]

        for i in range (1, len(candidates)):
            print('Tie Breaker Candidate ID:', candidates[i].id, 'Votes:', candidates[i].votes[choice])
            if next_choice < max_choices:
                if candidates[i].votes[next_choice] < min_votes:
                    min_votes = candidates[i].votes[next_choice]
                    min_candidate = candidates[i]

        if show_output is True:
            print('Returning minimum Candidate:', min_candidate.id)

        return min_candidate

    def get_pool_of_candidates(self):
        return [candidate for candidate in self.candidates if candidate.is_winner is None]


class CandidateEliminationSystem(VotingSystem):
    def __init__(self, candidates, ballots):
        super().__init__(candidates, ballots)
        #print('CandidateEliminationSystem __init__', [vars(candidate) for candidate in self.candidates])

    def count_ballots(self):
        candidate_cnt = len(self.candidates)
        choice_cnt = min(max_choices, candidate_cnt)

        # Count all first place votes to determine winner.
        while self.determine_winner() is not True:
            for vote_choice in range (0, choice_cnt):
                for i in range(0, candidate_cnt):
                    if self.candidates[i].is_winner is None: # Only count votes for candidates that are still in the pool.
                        self.candidates[i].total += self.candidates[i].votes[vote_choice]
                        print('Candidate', self.candidates[i].id, 'Total:', self.candidates[i].total)

                # After tallying "new" totals if there is still no majority, get the least voted candidate.
                loser = self.determine_loser()
                print('Loser:', loser.id)

                # Apply loser votes to other candidates.
                self.apply_loser_votes_to_other_candidates(loser, vote_choice)

                # Remove loser from candidate pool.
                loser_index = self.candidates.index(loser)
                self.candidates[loser_index].is_winner = False

        print('Ballots counted!')

        # Order candidates by points descending
        self.candidates = sort_candidates(self.candidates)

    # Apply the next place votes of the eliminated candidate to the first place of remaining candidates.
    def apply_loser_votes_to_other_candidates(self, loser, choice):
        print(f'Applying loser {loser.id}\'s votes to other candidates...')
        next_choice = choice + 1

        for i in range (0, len(self.ballots)):
            if self.ballots[i][choice] == loser.id:
                print(f'Voter {i} voted for loser {loser.id} at {place_str(choice, "p")}')
                if next_choice < max_choices:
                    next_choice_voted_id = self.ballots[i][next_choice]
                    print('Next choice voted candidate ID:', next_choice_voted_id)

                    if next_choice_voted_id != no_vote_val:
                        next_choice_index = map_id_to_candidate_index(next_choice_voted_id, self.candidates)
                        self.candidates[next_choice_index].total += 1
                        #print('Incremented total for ', vars(self.candidates[next_choice_index]))
                    else:
                        print(f'Voter {i} did not vote for {place_str(choice, "p")}.')

    # If two candidates have the same min/max values, break the tie by looking at the next place voted for count.
    def break_tie (self, candidate1, candidate2, mode, place, max_choices):
        next_place = place + 1

        if next_place < max_choices:
            if mode == 'min':
                if candidate1[next_place] < candidate2[next_place]:
                    return candidate1

                elif candidate1[next_place] == candidate2[next_place]:
                    return self.break_tie(candidate1, candidate2, mode, next_place, max_choices)

                else:
                    return candidate2
            elif mode == 'max':
                if candidate1[next_place] > candidate2[next_place]:
                    return candidate1
                elif candidate1[next_place] == candidate2[next_place]:
                    return self.break_tie(candidate1, candidate2, mode, next_place, max_choices)
                else:
                    return candidate2
        else:
            return None


# Tally votes based on weight
class WeightedVotingSystem(VotingSystem):
    def __init__(self, candidates, ballots):
        super().__init__(candidates, ballots)
        #print('WeightedVotingSystem __init__', [vars(candidate) for candidate in self.candidates])

        self.choice_vals = [1, 1 / 2, 1 / 4, 1 / 8]

    # Score candidate points based on votes ranked by choice.
    def count_ballots(self):
        total = 0
        for c in range (0, len(self.candidates)):
            for j in range (0, len(self.choice_vals)):
                total += self.candidates[c].votes[j] * self.choice_vals[j]

            self.candidates[c].total = total

    # Determine the winner based on the highest points and determine the winner based on the highest points.
    def determine_winner(self):
        if show_output is True:
            print('Determining winner...')

        winner_id = None
        total = 0
        tied_candidates = []

        for i in range (0, len(self.candidates)):
            # If a candidate has more points than the current points leader temporarily set that candidate as the winner.
            if self.candidates[i].total > total:
                total = self.candidates[i].total
                winner_id = self.candidates[i].id

            elif self.candidates[i].total == total:
                tied_candidates.append(self.candidates[i])

        if len(tied_candidates) > 0:
            # Set init placement to 0 for first place.
            choice = 0
            winner_id = self.break_tie(tied_candidates, choice)

        if winner_id is not None:
            self.winner_id = winner_id
        
            winner_index = map_id_to_candidate_index(self.winner_id, self.candidates)
            self.candidates[winner_index].is_winner = True
            print('Winner found! ', self.candidates[winner_index].name)
        else:
            print('No winner found.')

        # Order candidates by total descending.
        self.candidates = sort_candidates(self.candidates)


    # Tie breaking rules.
    # Call recursively
    def break_tie(self, tied_candidates, choice):
        print('Breaking tie...')
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
    
            if next_choice < max_choices:
                winner_id = self.break_tie(next_tied_candidates, next_choice)

        return winner_id


# Tally votes based on voters next choice
class NextChoiceSystem(VotingSystem):
    def __init__(self, candidates, ballots):
        super().__init__(candidates, ballots)
        #print('NextChoiceSystem __init__', [vars(candidate) for candidate in self.candidates])

    def count_ballots(self):
        print('\n\nCounting ballots...')
        candidate_cnt = len(self.candidates)

        # Count all first place votes to determine winner.
        # If no majority, count every voter's next choice votes and add to the total.
        # Exclude the losers votes
        # Calculate majority vote with total ballots * choice value.  Example: Second round
        voter_cnt = len(self.ballots)
        round_num = 1
        while self.determine_winner() is not True and round_num <= max_choices:

            # Reset total points for each candidate so we can count the next choice votes.
            # Update totals by counting the next choice votes.
            for i in range(0, candidate_cnt):
                self.candidates[i].total = 0

            for i in range(0, voter_cnt):
                ballot = self.ballots[i]

                # Note: since we're removing the loser from the ballot, we only need to count the top row.
                voted_id = ballot[0]

                if voted_id != no_vote_val:
                    index = map_id_to_candidate_index(voted_id, self.candidates)
                    self.candidates[index].total += 1
                    print('Round:', round_num, ' Voted ID:', voted_id, 'Total:', self.candidates[index].total)
                else:
                    print(f'Voter {i} did not vote for {place_str(0, "p")}.')

            # After tallying "new" totals if there is still no majority, get the least voted candidate.
            loser = self.determine_loser()

            # Remove loser from candidate pool and from all ballots.
            loser_index = self.candidates.index(loser)
            #print('Loser Index:', loser_index)
            self.candidates[loser_index].is_winner = False
            self.remove_loser_from_ballot(loser)

            round_num += 1

        # Order candidates by points descending
        self.candidates = sort_candidates(self.candidates)

    # Remove the loser candidate from all the ballots so they are not counted in the next round.
    def remove_loser_from_ballot(self, loser):
        #print(f'\nremove_loser_from_ballot({loser.id})')
        for i in range (0, len(self.ballots)):
            for j in range(len(self.ballots[i]) - 1, -1, -1):
                if self.ballots[i][j] == loser.id:
                    print('* Removing loser from ballot:', loser.id)
                    self.ballots[i].pop(j)
                    print('After removal:', self.ballots[i])

        print('Ballots after removal:', self.ballots)


# Run program
benchmark_id = uid(6)
print(f'\nStart Benchmark ID: {benchmark_id}')

elect = Election()
elect.register()
#elect.register_auto()
elect.vote()
elect.tally()

# Get scores and determine winner for Alaska system.
ces_candidates = elect.candidates
ces = CandidateEliminationSystem(ces_candidates, elect.ballots)
ces.count_ballots()

# Get scores and determine winner for alternative system: Weighted Voting System.
weight_candidates = elect.candidates
weight = WeightedVotingSystem(weight_candidates, elect.ballots)
weight.count_ballots()

# Get scores and determine winner for alternative system: Next Choice System.
ncs_candidates = elect.candidates
ncs = NextChoiceSystem(ncs_candidates, elect.ballots)
ncs.count_ballots()

# Show Results
elect.show_results(ces.candidates, weight.candidates, ncs.candidates)
print(f'End Benchmark ID: {benchmark_id}')

# End of program
