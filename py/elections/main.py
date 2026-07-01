# main.py

__author__ = "Jason Monroe (jason@jasonmonroe.com)"
__copyright__ = "Copyright Election Systems"
__date__ = "2025-01-24"
__version__ = "2.0.0"

# Python Libraries
from collections.abc import ValuesView
import logging
import sys

# Local Libraries
from src.constants import(ARG_PARAMS, I_BOT, I_WARNING)
from src.election import ElectionSys
from src.utils import get_run_id, init_logger, show_timer, start_timer

from voting_systems.last_remaining_candidate_sys import LastRemainingCandidateSystem
from voting_systems.popular_sys import PopularVotingSystem
from voting_systems.ranked_choice_sys import RankChoiceVotingSystem
from voting_systems.redistribution_sys import RedistributionSystem
from voting_systems.weighted_sys import WeightedSystem


def run_main_pipeline(args: dict, run_all: bool):
    logging.info(f"Run all voting systems: {run_all}")
   
    # Define electoral process: Select candidate count, declare candidacy
    election = ElectionSys(args.get('noise'))
    election.register()
    
    # --- Start the election season --- #
    election.campaign()
    election.vote()
    election.tally()

    # Note: Always create copies of the candidates and ballots!
    # Copy variables for scoring
    candidates = election.candidates
    voters = election.voters

    # --- Now compare results to different systems --- #

    if run_all or args.get('popular'):
        # Popular Vote System
        popular_sys = PopularVotingSystem(candidates.copy(), voters.copy())
        logging.info("Running " +popular_sys.title.title() )
        popular_sys.results()
        popular_sys.show_results()

    if run_all or args.get("ranked"):
        # Ranked Choice Voting System
        ranked_choice_sys = RankChoiceVotingSystem(candidates.copy(), voters.copy())
        logging.info("Running " + ranked_choice_sys.title.title())
        ranked_choice_sys.results()
        ranked_choice_sys.show_results()
         
    if run_all or args.get("redist"):
     
        # Redistribution System
        redistribution_sys = RedistributionSystem(candidates.copy(), voters.copy())
        logging.info("Running " + redistribution_sys.title.title())
        redistribution_sys.results()
        redistribution_sys.show_results()

    if run_all or args.get("remaining"):
        # Remaining Candidates System
        last_remaining_sys = LastRemainingCandidateSystem(candidates.copy(), voters.copy())

    if run_all or args.get("weighted"):
        # Weighted System
        weighted_sys = WeightedSystem(candidates.copy(), voters.copy())



    
    # Final Results
    subtitles = election.results

def _run_all_voting_sys(args: dict) -> bool:
    all_sys = all(args.values())
    no_sys = not any(args.values())

    return all_sys or no_sys


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

    args = _parse_args(sys.argv[1:])
    run_all = _run_all_voting_sys(args)     
    logger = init_logger(run_id, args.get("debug"))
    
    print(f"\n==== {I_BOT} START RUN ID: {run_id} {I_BOT} ====")
    logging.info(f"\n==== {I_BOT} START RUN ID: {run_id} {I_BOT} ====")
    
    # --- Start --- #
    run_main_pipeline(args, run_all)

    show_timer(start_time) 
    print(f"\n==== {I_BOT} END   RUN ID: {run_id} {I_BOT} ====\n")
    logging.info(f"\n==== {I_BOT} END   RUN ID: {run_id} {I_BOT} ====\n")
