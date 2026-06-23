# src/utils.py

"""
+----------------------------------------------------------------------------
| Utilities
+----------------------------------------------------------------------------
| Utility functions used as helpers.
"""

# Python Libraries
import random
import textwrap
import time
import uuid

from src.candidate import Candidate
from src.constants import (I_TIMER, MAX_LINE_LEN, MSEC, PEP8_LINE_LEN, RUN_MAX_ID, RUN_MIN_ID, SECS_IN_MIN)

def get_run_id() -> str:
    """ Generates a unique ID for the current run. """
    return str(random.randint(RUN_MIN_ID, RUN_MAX_ID))


def gen_uuid(len:int | None) -> str:

    uid = uuid.uuid4().hex.lower()
    if len is None:
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
    print(f"{I_TIMER} Run Time: {get_time(start_time_int)}")


def _make_top_btm_line() -> str:
    #open_close_len = 2 # open close of char `+` or `|`
    #max_line_len = PEP8_LINE_LEN - open_close_len

    return '+' + ('-' * (PEP8_LINE_LEN - 2)) + '+'


def _create_title_banner(text: str, center_text: bool=True) -> None:
    open_close_len = 4 # open close of char `+` or `|`
    #max_line_len = PEP8_LINE_LEN - open_close_len

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
        
    top_btm_line = _make_top_btm_line()

    # Print title banner
    print("\n")
    print(top_btm_line)
    print(title_line)
    print(top_btm_line)


def _create_subtitle_banner(text: str | list, center_text: bool=False) -> None:
    # Reconstructs the guard to safely catch wrong types OR empty values
    if not isinstance(text, (str, list)) or not text:
        print('return None')
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
       
    # Close the subtitle
    if len(wrapped_lines) > 0:
        print(_make_top_btm_line())

    return None


def show_banner(title: str, subtitle: str | list | None="", center_title_text: bool=True, center_subtitle_text: bool=False) -> None:
    _create_title_banner(title, center_title_text)

    if subtitle:
        _create_subtitle_banner(subtitle, center_subtitle_text)


def get_index_by_uid(candidates: list, uid: str) -> int | None:
    return next((i for i, candidate in enumerate(candidates) if candidate.uid == uid), None)


def get_candidate_by_uid(candidates: list, uid: str):
    return next((candidate for candidate in candidates if candidate.uid == uid), None)


def placement(place: int, mode: str) -> str:
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

