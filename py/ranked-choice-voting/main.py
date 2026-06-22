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
from src.election 
from src.utils import get_run_id, show_banner, show_timer, start_timer

def run_main_pipeline():

    # Validate input: 
    candidate_cnt = 0
    candidates = []

    # Define electoral process: Select candidate count, declare candidacy

    # Declare candidacies
    # Register to vote

    # Display Candidate count, voter count

    # tally and count votes
    # save results

    # Now compare results to different systems

    

    pass


def _validate_input(message: str, str_flag: bool=False):
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
    run_id = get_run_id()
    print(f'\n==== {I_BOT} START RUN ID: {run_id} {I_BOT} ====\n')

    show_banner('ELECTION SYSTEMS')

    args = _parse_args(sys.argv[1:])
    print(f'args = {args}')
    
    # --- Start --- #
    run_main_pipeline()


    show_timer(start_time) 
    print(f'\n==== {I_BOT} END   RUN ID: {run_id} {I_BOT} ====\n')
    