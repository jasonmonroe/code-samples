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
from src.constants import( ARG_PARAMS, I_BOT, I_WARNING)
from src.election import ElectionSys
from src.utils import get_run_id, show_banner, show_timer, start_timer
from voting_systems.last_remaining_candidate_sys import LastRemainingCandidateSystem
from voting_systems.popular_sys import PopularVotingSystem
from voting_systems.ranked_choice_sys import RankChoiceVotingSystem
from voting_systems.redistribution_sys import RedistributionSystem
from voting_systems.weighted_sys import WeightedSystem



 
def run_main_pipeline(args: dict):

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
        #sys.exit(1)

    return {arg.strip('--'): (arg in command_line_args) for arg in ARG_PARAMS}


# Set logging information
class ClassNameFilter(logging.Filter):
    def filter(self, record):
        # Default value if the log isn't called from inside a class method
        record.classname = "Module"
        frame = inspect.currentframe()

        while frame:
            filename = frame.f_code.co_filename
            func_name = frame.f_code.co_name
            func_name_str = func_name + "()"
             
            # 1. Skip standard logging library files
            if "logging" in filename:
                frame = frame.f_back
                continue
                
            # 2. Skip this filter's own internal method frame
            if func_name == "filter" or "ClassNameFilter" in func_name:
                frame = frame.f_back
                continue
                
            # 3. Check for the user's class instance 'self'
            if 'self' in frame.f_locals:
                obj = frame.f_locals['self']
                # Ensure 'self' is not the filter instance itself
                if obj.__class__.__name__ != "ClassNameFilter":
                    record.classname = obj.__class__.__name__
                    break
                
            frame = frame.f_back
            
        return True
 
def _set_logger(run_id: str):
    print("# --- Setting logger --- #")
    project_dir = Path(__file__).resolve().parent
    log_dir = project_dir / "logs"
    
    # Safely creates folder if it doesn't exist (no IF check needed)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Define shared formatter
    formatter = logging.Formatter('%(asctime)s - %(classname)s.%(funcName)s - %(levelname)s - %(message)s')
    
    # SETUP MAIN/ROOT LOGGER (output-{run_id}.log)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    main_file_path = log_dir / f"output-{run_id}.log"
    main_handler = logging.FileHandler(filename=str(main_file_path), mode='a')
    main_handler.setLevel(logging.DEBUG)
    main_handler.setFormatter(formatter)
    root_logger.addHandler(main_handler)

    # SETUP TOPIC LOGGER (results-{run_id}.log)
    results_log = logging.getLogger("results_logger")
    results_log.setLevel(logging.INFO)
    results_log.propagate = False  # Prevents results logs from leaking into output.log
    results_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    if results_log.hasHandlers():
        results_log.handlers.clear()

    results_file_path = log_dir / f"results-{run_id}.log"
    results_handler = logging.FileHandler(filename=str(results_file_path), mode='a')
    results_handler.setLevel(logging.INFO)
    results_handler.setFormatter(results_formatter)
    results_log.addHandler(results_handler)

    # 3. ATTACH FILTERS GLOBALLY
    if not any(isinstance(f, ClassNameFilter) for f in root_logger.filters):
        root_logger.addFilter(ClassNameFilter())
        
    if not any(isinstance(f, ClassNameFilter) for f in results_log.filters):
        results_log.addFilter(ClassNameFilter())
        
    return logging.getLogger(__name__)


if __name__ == "__main__":
    start_time = start_timer()

    run_id = get_run_id()    
    logger = _set_logger(run_id)
    print(f'\n==== {I_BOT} START RUN ID: {run_id} {I_BOT} ====\n')
    logging.info(f'\n==== {I_BOT} START RUN ID: {run_id} {I_BOT} ====\n')

    logging.info("\nELECTION SYSTEMS")
    show_banner('ELECTION SYSTEMS')

    args = _parse_args(sys.argv[1:])
    print(f'args = {args}')

    
    # --- Start --- #
    run_main_pipeline(args)

    show_timer(start_time) 
    print(f'\n==== {I_BOT} END   RUN ID: {run_id} {I_BOT} ====\n')
    logging.info(f'\n==== {I_BOT} END   RUN ID: {run_id} {I_BOT} ====\n')