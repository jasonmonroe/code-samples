# main.py

__author__ = "Jason Monroe (jason@jasonmonroe.com)"
__copyright__ = "Copyright Election Systems"
__date__ = "2025-01-24"
__version__ = "1.0.0"

# Python Libraries
import inspect
import logging
from pathlib import Path
import sys

# Local Libraries
from src.class_name_filter import ClassNameFilter
from src.constants import( ARG_PARAMS, I_BOT, I_WARNING)
from src.election import ElectionSys
from src.utils import get_run_id, init_logger, show_banner, show_timer, start_timer
from voting_systems.last_remaining_candidate_sys import LastRemainingCandidateSystem
from voting_systems.popular_sys import PopularVotingSystem
from voting_systems.ranked_choice_sys import RankChoiceVotingSystem
from voting_systems.redistribution_sys import RedistributionSystem
from voting_systems.weighted_sys import WeightedSystem


def run_main_pipeline(args: dict):

    print(f'run_main_pipeline({args})')

    # Define electoral process: Select candidate count, declare candidacy
    election = ElectionSys(args.get('noise'))

    voter_cnt = election.register()
    election.contribute(voter_cnt)
    election.vote(voter_cnt)
    election.tally()

    # Copy variables for scoring
    candidates = election.candidates
    ballots = election.ballots

    # --- Now compare results to different systems --- #

    # Note: Always create copies of the candidates and ballots!

    """
    # Popular Vote System
    print("Running Popular Vote System...")
    logging.info("Popular Vote System")

    popular_sys = PopularVotingSystem(candidates.copy(), ballots.copy())
    #popular_sys.tally_totals()
    #popular_sys.determine_winner()
    popular_sys.results()
    popular_sys.show_results()
    """


    # Ranked Choice Voting System
    ranked_choice_sys = RankChoiceVotingSystem(candidates.copy(), ballots.copy())
    logging.info("Running " + ranked_choice_sys.title)
    ranked_choice_sys.results()
    ranked_choice_sys.show_results()
     

    
    # Redistribution System
    #redistribution_sys = RedistributionSystem(candidates.copy(), ballots.copy())

    # Remaining Candidates System
    #last_remaining_sys = LastRemainingCandidateSystem(candidates.copy(), ballots.copy())

    # Weighted System
    #weighted_sys = WeightedSystem(candidates.copy(), ballots.copy())



    
    # Final Results
    subtitles = election.results

def _parse_args(command_line_args: list[str]) -> dict:
    """
    Parse arguments present in command line.
    :param command_line_args:
    :return:
    """
    if len(command_line_args) == 0:
        print(f'{I_WARNING} No args present... {I_WARNING}')
       
    return {arg.strip('--'): (arg in command_line_args) for arg in ARG_PARAMS}

if __name__ == "__main__":
    start_time = start_timer()

    run_id = get_run_id()    
    logger = init_logger(run_id)

    print(f'\n==== {I_BOT} START RUN ID: {run_id} {I_BOT} ====')
    logging.info(f'\n==== {I_BOT} START RUN ID: {run_id} {I_BOT} ====')

    logging.info("\nELECTION SYSTEMS")
    show_banner('ELECTION SYSTEMS')

    args = _parse_args(sys.argv[1:])
    
    # --- Start --- #
    run_main_pipeline(args)

    show_timer(start_time) 
    print(f'\n==== {I_BOT} END   RUN ID: {run_id} {I_BOT} ====\n')
    logging.info(f'\n==== {I_BOT} END   RUN ID: {run_id} {I_BOT} ====\n')
