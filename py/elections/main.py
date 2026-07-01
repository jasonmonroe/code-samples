# main.py

__author__ = "Jason Monroe (jason@jasonmonroe.com)"
__copyright__ = "Copyright Election Systems"
__date__ = "2025-01-24"
__version__ = "2.0.0"

# Python Libraries
import copy
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
    election = ElectionSys(args.get("noise"))
    election.register()
    
    # --- Start the election season --- #
    election.campaign()
    election.vote()
    election.tally()

    # Note: Always create copies of the candidates and ballots!
    # Copy variables for scoring
    candidates = election.candidates.copy()
    voters = election.voters.copy()

    # --- Now compare results to different systems --- #
    popular_sys, ranked_choice_sys, redistribution_sys, last_remaining_sys = None, None, None, None

    if run_all or args.get('popular'):
        popular_sys = PopularVotingSystem(copy.deepcopy(candidates), copy.deepcopy(voters))
        logging.info("Running " + popular_sys.title.title())
        popular_sys.results()
        popular_sys.show_results()
        
    if run_all or args.get("ranked"):
        ranked_choice_sys = RankChoiceVotingSystem(copy.deepcopy(candidates), copy.deepcopy(voters))
        logging.info("Running " + ranked_choice_sys.title.title())
        ranked_choice_sys.results()
        ranked_choice_sys.show_results()
        
    if run_all or args.get("redist"):
        redistribution_sys = RedistributionSystem(copy.deepcopy(candidates), copy.deepcopy(voters))
        logging.info("Running " + redistribution_sys.title.title())
        redistribution_sys.results()
        redistribution_sys.show_results()
        
    if run_all or args.get("remaining"):
        last_remaining_sys = LastRemainingCandidateSystem(copy.deepcopy(candidates), copy.deepcopy(voters))
        logging.info("Running " + last_remaining_sys.title.title())
        last_remaining_sys.results()
        last_remaining_sys.show_results()

    if run_all or args.get("weighted"):
        weighted_sys = WeightedSystem(copy.deepcopy(candidates), copy.deepcopy(voters), args.get("noise"))
        logging.info("Running" + weighted_sys.title.title())

        all_candidates = {}

        if popular_sys:
            all_candidates["popular"] = popular_sys._pool.get().copy()
        if ranked_choice_sys:
            all_candidates["ranked"] = ranked_choice_sys._pool.get().copy()
        if redistribution_sys:
            all_candidates["redist"] = redistribution_sys._pool.get().copy()
        if last_remaining_sys:
            all_candidates["remaining"] = last_remaining_sys._pool.get().copy()
       
        if len(all_candidates):
            weighted_sys.results(all_candidates)
            weighted_sys.show_results()
        else:
            logging.warning("No voting systems rendered to weight.")


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
    logger = init_logger(run_id, args.get("debug"), args.get("no_log"))
    
    print(f"\n==== {I_BOT} START RUN ID: {run_id} {I_BOT} ====")
    logging.info(f"\n==== {I_BOT} START RUN ID: {run_id} {I_BOT} ====")
    
    # --- Start --- #
    run_main_pipeline(args, run_all)

    show_timer(start_time) 
    print(f"\n==== {I_BOT} END   RUN ID: {run_id} {I_BOT} ====\n")
    logging.info(f"\n==== {I_BOT} END   RUN ID: {run_id} {I_BOT} ====\n")
