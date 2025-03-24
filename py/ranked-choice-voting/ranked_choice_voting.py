"""
|--------------------------------------------------------------------------
| Ranked Choice Voting
|--------------------------------------------------------------------------
| Jason Monroe
| jason@jasonmonroe.com
| ranked_choice_voting.py
|
| January 19, 2025
|--------------------------------------------------------------------------
| Overview:  Voters approved a revamp of the election season where no longer
| is it who gets the most votes wins the election but now a rank-choice voting
| system that takes into account overall voter sentiment.
|
| This system allows voters to rank their choices in order of preference. If
| a candidate receives more than half of the first choice votes, they win.
|
| This is a script to run multiple elections to determine a winner by a ranked
| choice.
| The systems are: Point Score, Remaining Candidates, Redistribution,
| Voted-Weighted Systems
"""

# Import Libraries
from election import Election
from helpers import uid, show_output

from all_voting_sys_weighted import AllVotingWeightedSystem
from popular_vote_sys import PopularVoteSystem
from redistribution_sys import RedistributionSystem
from rem_candidates_sys import RemainingCandidatesSystem
from weighted_score_sys import WeightedScoreSystem


### Run Program
benchmark_id = uid(6)
print(f'\n* Start Benchmark ID: {benchmark_id} *')

# Create and run election
elect = Election()
elect.election_day()

# Make copies of the candidates and ballots for each system. This is to ensure the original data is not modified.
ballots = elect.ballots.copy()
candidates = elect.candidates.copy()


# Popular Vote System
popular_candidates = candidates.copy()
popular = PopularVoteSystem(popular_candidates, ballots.copy())
popular.score_ballots()
popular_candidates = popular.determine_winner_by_popular()
elect.show_results('popular')
elect.save_results(popular.title, popular_candidates)

# Tally Weighted Score System
weight_candidates = candidates.copy()
weight = WeightedScoreSystem(weight_candidates, ballots.copy())
weight.score_ballots()
weight_candidates = weight.determine_winner_by_popular()
elect.show_results()
elect.save_results(weight.title, weight_candidates)

# Tally Remaining Candidates System
rem_candidates = candidates.copy()
rem = RemainingCandidatesSystem(rem_candidates, ballots.copy())
rem.score_ballots()
#rem.determine_winner_by_majority()
elect.show_results()
elect.save_results(rem.title, rem_candidates)

# Tally Redistribution System
redistribution_candidates = candidates.copy()
redistribution = RedistributionSystem(redistribution_candidates, ballots.copy())
redistribution.score_ballots()
#redistribution.determine_winner_by_majority()
elect.show_results()
elect.save_results(redistribution.title, redistribution_candidates)

# Tally Average-Weighted Systems
all_sys = AllVotingWeightedSystem(elect.results)
all_sys.show_totals_by_sys()
all_sys.determine_winner()

# Show Results
print(f'\n* End Benchmark ID: {benchmark_id} *')

### End of Program
