# src/utils.py
"""
+----------------------------------------------------------------------------
| Utilities
+----------------------------------------------------------------------------
| Utility functions used as helpers.
"""

# Python Libraries
from datetime import datetime
from pathlib import Path
import logging
import random
import textwrap
import time
import uuid
from statistics import mean

# Local Libraries
from src.class_name_filter import ClassNameFilter
from src.constants import (
    I_TIMER, 
    MAX_LINE_LEN, 
    MSEC, 
    PEP8_LINE_LEN, 
    PERCENTILE, 
    RUN_MAX_ID, 
    RUN_MIN_ID, 
    SECS_IN_MIN
    )

results_logger = logging.getLogger("results_logger")

# --- General Helpers --- #
def get_run_id() -> str:
    """ Generates a unique ID for the current run. """
    return str(random.randint(RUN_MIN_ID, RUN_MAX_ID))


def gen_uuid(len:int | None) -> str:

    uid = uuid.uuid4().hex.lower()
    if not len:
        return uid

    return uid[0: len]
    

def start_timer() -> float:
    """
    Start a timer
    """
    return time.time()


def get_time(start_time_float: float, end_time_float: float | None = None) -> str:
    
    if end_time_float is None:
        end_time_float = time.time()

    diff = abs(end_time_float - start_time_float)
    _, remainder = divmod(diff, SECS_IN_MIN*SECS_IN_MIN)
    minutes, seconds = divmod(remainder, SECS_IN_MIN)
    fractional_seconds = seconds - int(seconds)

    ms = fractional_seconds * MSEC
    return f"{int(minutes)}m {int(seconds)}s {int(ms)}ms"


def show_timer(start_time_int: float) -> None:
    msg = f"{I_TIMER} Run Time: {get_time(start_time_int)}"
    print(msg)
    logging.info(msg)


def _draw_line() -> str:
    return '+' + ('-' * (PEP8_LINE_LEN - 2)) + '+'


def _create_title_banner(text: str, center_text: bool=True) -> None:
    open_close_len = 4 # open close of char `+` or `|`
    
    # Trim off any chars after limit plus two spaces for blanks
    text = text[0: MAX_LINE_LEN - open_close_len]
    text_len = len(text)
    padding_len = MAX_LINE_LEN - text_len    
   
    if center_text:
        # If uneven padding add an extra length for the right side
        extra_len = 0 if padding_len % 2 == 0 else 1
      
        padding_len = padding_len // 2
        title_line = "| " + (' ' * padding_len) + text + (' ' * (padding_len + extra_len)) + " |"
    
    else:
        # Remove last two characters to account for open/close spacing
        title_line = "| " + text + (' ' * padding_len) + " |"
        
    top_btm_line = _draw_line()

    # Print title banner
    print("")
    print(top_btm_line)
    print(title_line)
    print(top_btm_line)

    results_logger.info(top_btm_line)
    results_logger.info(title_line)
    results_logger.info(top_btm_line)


def _create_subtitle_banner(text: str | list, center_text: bool=False) -> None:
    # Reconstructs the guard to safely catch wrong types OR empty values
    if not isinstance(text, (str, list)) or not text:
        logging.error('Text is not a string or list.  Invalid type.')
        return None
        
    open_close_len = 4 # open close of char `+` or `|` plus space
    max_line_len = PEP8_LINE_LEN - open_close_len 
    wrapped_lines = []

    if isinstance(text, list):
        wrapped_lines = text
   
    elif isinstance(text, str):
        wrapped_lines = textwrap.wrap(text, width=max_line_len)

    # Now that the data is a list format it for display.
    for line in wrapped_lines:
        if "\n" in line:
            line = ""

        line_len = len(line)
    
        padding_len = max_line_len - line_len
      
        if center_text:    
            extra_len = 0 if padding_len % 2 == 0 else 1
            padding_len = padding_len // 2
            padded_line = "| " + (' ' * padding_len) + line + (' ' * (padding_len + extra_len)) + " |"
        else:
            padded_line = "| " + line + (' ' * padding_len) + " |"
  
        print(padded_line)
        results_logger.info(padded_line)
       
    # Close the subtitle
    if len(wrapped_lines) > 0:
        print(_draw_line())
        results_logger.info(_draw_line())

    return None


def show_banner(title: str, subtitle: str | list | None="", center_title_text: bool=True, center_subtitle_text: bool=False) -> None:
    _create_title_banner(title, center_title_text)

    if subtitle:
        _create_subtitle_banner(subtitle, center_subtitle_text)


# --- App based helpers --- #
def calc_pct_change(start: float, final: float) -> float:
    return round(((final - start) / start) * PERCENTILE, 1)


def optimize_index_by_uid(uid: str, candidates: dict) -> int | None:
    # Instant O(1) lookup, no matter how many millions of items exist
    if uid in candidates:
        return candidates[uid]
    pass


def get_index_by_uid(candidates: list, uid: str) -> int | None:
    return next((i for i, candidate in enumerate(candidates) if candidate.uid == uid), None)


def get_candidate_by_uid(candidates: list, uid: str):
    return next((candidate for candidate in candidates if candidate.uid == uid), None)

def name_len(candidates: dict) -> dict:
        if not candidates:
            return {"mean": 0, "max": 0}

        lenghts = [len(c.name) for c in candidates]

        return {"mean": int(mean(lenghts)), "max": int(max(lenghts))}

def placement(place: int, mode: str="") -> str:
    """
    Get the placement string for a candidate.

    :param int place: What order of placement.
    :param string mode: What type of placement string to output.

    :return: string attrs[place]: String of the placement.
    """
    if mode == 'a':
        attrs = ['first', 'second', 'third', 'fourth']
    else:
        attrs = ['1st Place', '2nd Place', '3rd Place', '4th Place']

    return attrs[place]


def init_logger(run_id: str, debug_flag: bool=False) -> logging.Logger:
    logging.debug("# --- Setting logger --- #")

    logging_type = logging.DEBUG if debug_flag else logging.INFO
    
    project_dir = Path(__file__).resolve().parent.parent
    logging.info(f"Project Dir: {project_dir}")
    
    log_dir = project_dir / "logs"
    logging.info(f"Log Dir: {log_dir}")
    
    # Safely creates folder if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate the safe datetime string (e.g., "2026-06-25_23-18-18")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Updated: Added line number with 3-space right-alignment padding directly before classname
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(classname)s.%(funcName)s - %(lineno)3d - %(message)s')
    
    # SETUP MAIN/ROOT LOGGER
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    output_file_path = log_dir / f"{timestamp}_output.log"
    output_handler = logging.FileHandler(filename=str(output_file_path), mode='a')
    output_handler.setLevel(logging_type)  
    output_handler.setFormatter(formatter)
    root_logger.addHandler(output_handler)
    
    # SETUP TOPIC LOGGER
    results_log = logging.getLogger("results_logger")
    results_log.setLevel(logging.INFO)
    results_log.propagate = False 
    
    results_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    if results_log.hasHandlers():
        results_log.handlers.clear()
        
    results_file_path = log_dir / f"{timestamp}_results.log"
    results_handler = logging.FileHandler(filename=str(results_file_path), mode='a')
    results_handler.setLevel(logging.INFO)
    results_handler.setFormatter(results_formatter)
    results_log.addHandler(results_handler)
    
    # ATTACH FILTERS GLOBALLY
    if not any(isinstance(f, ClassNameFilter) for f in root_logger.filters):
        root_logger.addFilter(ClassNameFilter())
        
    if not any(isinstance(f, ClassNameFilter) for f in results_log.filters):
        results_log.addFilter(ClassNameFilter())
        
    return logging.getLogger(__name__)
    

def mute_logger(candidate_cnt: int, voter_cnt:int):
    logging.critical(f"Candidates: {candidate_cnt}, Voters: {voter_cnt} is too high.\n # --- 🚩 Turning off logs. 🚩 --- #")
    logging.getLogger("results_logger").setLevel(logging.CRITICAL + 1)


"""
# Finds the index of the first object where name is "Bob"
bob_index = next((i for i, u in enumerate(users) if u.name == "Bob"), None)

print(bob_index)


Remove by uid

# 1. Find the index of the unique name (returns None if not found)
idx = next((i for i, u in enumerate(users) if u.name == "Bob"), None)

# 2. Remove it if it exists
if idx is not None:
    removed_user = users.pop(idx)  # Optional: 'removed_user' now holds the deleted object

users[:] = [u for u in users if u.name != "Bob"]
arr[:] = [a for a in arr if a.key != "___"]


# Get highest voted 
return [max(candidates, key=lambda c: c.total)]
return [max(candidates, key=lambda c: c.votes[choice])]

+-----------------------------------------------------------------------------+
|                               BALLOT TALLIES                                |
+-----------------------------------------------------------------------------+
|      VOTES    | Candidate                                                   |
| [4, 2, 3, 5] | 8f30ec - (LIB) Aries Schmidt                                 |
| [2, 5, 5, 2] | fc8aee - (GRE) Samuel Davis                                  |
| [6, 5, 2, 1] | 98f74c - (DEM) Ava Ivanov                                    |
| [2, 2, 4, 6] | b4fae9 - (FOR) Lars Gonzalez                                 |
+-----------------------------------------------------------------------------+
"""