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
from src.constants import( ARG_PARAMS, DEFAULT_CANDIDATE_COUNT, DEFAULT_VOTER_COUNT, I_BOT, I_WARNING, MAX_CANDIDATES, MIN_CANDIDATES)
from src.election import ElectionSys
from src.utils import get_run_id, show_banner, show_timer, start_timer

def run_main_pipeline():
    
    print('run_main_pipeline()')


    # Validate input: 


    # Define electoral process: Select candidate count, declare candidacy
    election = ElectionSys()
    voter_cnt = election.register()
    election.vote(voter_cnt)
    election.tally()
    

    # Declare candidacies
    # Register to vote

    # Display Candidate count, voter count

    # tally and count votes
    # save results

    # Now compare results to different systems

    

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
    