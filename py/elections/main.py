# main.py

__author__ = "Jason Monroe (jason@jasonmonroe.com)"
__copyright__ = "Copyright Election Systems"
__date__ = "2025-01-24"
__version__ = "1.0.0"

# Python Libraries
import logging
import os
import sys

# Local Libraries
from src.constants import( ARG_PARAMS, I_BOT, I_WARNING)
from src.election import ElectionSys
from src.utils import get_run_id, show_banner, show_timer, start_timer
from voting_systems.last_remaining_candidate_sys import LastRemainingCandidateSystem
from voting_systems.popular_sys import PopularVotingSystem
from voting_systems.ranked_choice_sys import RankChoiceVotingSystem
from voting_systems.redistribution_sys import RedistributionSystem
from voting_systems.weighted_sys import WeightedSystem

def run_main_pipeline():

    print('run_main_pipeline()')


    # Define electoral process: Select candidate count, declare candidacy
    election = ElectionSys()
    voter_cnt = election.register()
    election.contribute(voter_cnt)
    election.vote(voter_cnt)
    election.tally()

    # Copy variables for scoring
    candidates = election.candidates
    ballots = election.ballots

    # --- Now compare results to different systems --- #

    # Popular Vote System
    print("Running Popular Vote System...")
    logging.info("Popular Vote System")
    # Note: Always create copies of the candidates and ballots!
    
    popular_sys = PopularVotingSystem(candidates.copy(), ballots.copy())
    popular_sys.calc_totals()
    popular_sys.determine_winner()
    popular_sys.show_results()


    # Ranked Choice Voting System
    #print("Running Ranked")
    #ranked_choice_sys = RankChoiceVotingSystem(candidates.copy(), ballots.copy())
     

    
    # Redistribution System
    #redistribution_sys = RedistributionSystem(candidates.copy(), ballots.copy())

    # Remaining Candidates System
    #last_remaining_sys = LastRemainingCandidateSystem(candidates.copy(), ballots.copy())

    # Weighted System
    #weighted_sys = WeightedSystem(candidates.copy(), ballots.copy())



    

    pass




def _parse_args(command_line_args: list[str]) -> dict:
    """
    Parse arguments present in command line.
    :param command_line_args:
    :return:
    """
    if len(command_line_args) == 0:
        print(f'{I_WARNING} No args present... {I_WARNING}')
        #sys.exit(1)

    return {arg.strip('--'): (arg in command_line_args) for arg in ARG_PARAMS}


if __name__ == "__main__":
    start_time = start_timer()

    logger = logging.getLogger(__name__)
    logging.basicConfig() 
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    

    run_id = get_run_id()
    print(f'\n==== {I_BOT} START RUN ID: {run_id} {I_BOT} ====\n')

    show_banner('ELECTION SYSTEMS')

    args = _parse_args(sys.argv[1:])
    print(f'args = {args}')
    
    # --- Start --- #
    run_main_pipeline()

    show_timer(start_time) 
    print(f'\n==== {I_BOT} END   RUN ID: {run_id} {I_BOT} ====\n')
    