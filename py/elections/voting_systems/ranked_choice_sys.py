# voting_systems/ranked_choice_sys.py

"""
+----------------------------------------------------------------------------
| RANK CHOICE VOTING SYSTEM
+----------------------------------------------------------------------------
| This system is used by the state of Alaska. Instead of choosing one candidate,
| you fill in the oval in column one for the candidate you would most like to win,
| then vote for your second choice in column two and so on.  Ranking other candidates
| does not impact your first choice, and you do not have to rank them all.  You should
| only mark one oval in each row and one oval in each column.
|
| The ballots are tallied and scored by its first choice votes.  If a candidate
| gets at least half of the votes in round one, they win.  If this doesn't happen, it's
| continued to next round and the candidate with the least nth choice votes is eliminated.
| Count the voter's next remaining candidate choice instead of their choice for the
| eliminated candidate (meaning they still have a say in whom wins).
|
| Repeat these steps in rounds until there are only two candidates and now whomever
| has the most votes is determined the winner.

| @link https://www.elections.alaska.gov/election-information/
| @link https://www.youtube.com/watch?v=lLU3lbrxMBI
| @link https://www.youtube.com/watch?v=oHRPMJmzBBw
"""

# Python Libraries
import logging

# Local Libraries
from src.candidate import Candidate
from src.constants import FIRST_CHOICE, I_RIBBON, MAX_CHOICES
from src.utils import get_index_by_uid, placement, show_banner
from voting_systems.base_voting_sys import BaseVotingSystem


 

class RankChoiceVotingSystem(BaseVotingSystem):
    def __init__(self, candidates: list, ballots: list):
        super().__init__(candidates, ballots) 
        
        self.title = "Rank Choice Voting" + self.title

    def results(self):
        #choice = FIRST_CHOICE

        for round in range(0, MAX_CHOICES):
            logging.debug(f"choice={round}, {placement(round, 'a')} round...")

            # Important: Always count the first choice regardless of round
            # because the loser will have their names removed from the ballots!
            self.tally_totals(FIRST_CHOICE, True, True) 

            # Any candidate have a majority?
            for candidate in self.candidate_pool:
                logging.debug(f"line 55: determine if {candidate.uid} is the  winner...")
                if self.determine_winner(candidate):
                    break
                
            if self.winner is not None:
                break

            # If no winner, remove lowest performing candidate
            logging.debug(f"No winner in round: {placement(round, 'a')}.")

            # Remove lowest candidate
            loser_candidate = self.determine_loser(round)

            # Remove loser candidate pool and ballots
            if loser_candidate is not None:
                loser_idx = get_index_by_uid(self.candidate_pool, loser_candidate.uid)
                self.candidate_pool.pop(loser_idx)

                self.shift_ballots(loser_candidate.uid)
                

        # Break full loop
        logging.debug("LOOP BREAK...")





        """
        
        while len(self.candidate_pool) > 1 and choice < MAX_CHOICES:
            highest = []
            highest_total = 0
            self.tally_totals(choice, False, True)

            for candidate in self.candidate_pool:
                if candidate.total > highest_total:
                    highest_total = candidate.total
                    highest = [candidate]
                elif candidate.total == highest_total:
                    highest.append(candidate)
                else:
                    pass
        """



    def determine_winner(self, candidate: Candidate) -> bool:
        logging.debug(f"determine_winner() - CHECKING: if {candidate.total} >= {self.majority} ?")
        #print(f"determine_winner() - CHECKING: if {candidate.total} >= {self.majority} ?")
        
        if candidate.total >= self.majority:
            self.winner = candidate
            return True
        
        return False
        
        
    def determine_loser(self, choice: int=FIRST_CHOICE) -> Candidate | None:
        # Let's assume that the loser has less than a majority
        #print("determine_loser()")
        lowest = []
        lowest_total = self.majority - 1
        loser_pool = self.candidate_pool.copy()
        #itr = 0
        #choice
        while len(loser_pool) > 1 and choice < MAX_CHOICES:
            for candidate in loser_pool:
                # Use next place vote count as threshold, NOT calculating a new total
                #if candidate.total < lowest_total:
                if candidate.votes[choice] < lowest_total:
                    #lowest_total = candidate.total
                    lowest_total = candidate.votes[choice]
                    lowest = [candidate]
                #elif candidate.total == lowest:
                elif candidate.votes[choice] == lowest:
                    lowest.append(candidate)

            if len(lowest) == 1:
                return lowest[0]

            # Tied!
            if len(lowest) > 1:
                msg = f"We have {len(lowest)} candidates tied at {lowest_total} for lowest votes."
                logging.info(msg)
                #print(msg)
                # What if the losing candidates tie for last place? Who gets removed?
                loser_pool = lowest
                
            choice += 1

        msg = f"Did not have a losing candidate."
        logging.warning(msg)
      
        return None


                   
    def shift_ballots(self, loser_uid: str) -> None:
        logging.debug("shift_ballots()")
     
        logging.debug(f"Loser UID: {loser_uid}")

        for ballot in self.ballots:
            #print(f"Ballot = {ballot}")
            for candidate_choice in ballot:
                if candidate_choice == loser_uid:
                    ballot.remove(candidate_choice)

    """
    def show_results(self) -> None:
        if self.winner:
            subtitles = []
            for candidate in self.candidates:
                line = f"Candidate: {candidate.name} | Total: {candidate.total}"
                subtitles.append(line)

            show_banner(self.title, subtitles)
            print(f"\nWinner: {I_RIBBON} {self.winner.name} ({self.winner.party})\n")
        
        else:
            logging.warning("No winner!")
            show_banner(self.title, "No winner!")
            
        self.candidate_pool = []


    
    def results1(self):
        #choice = FIRST_CHOICE

        end_count = False
        for vote_choice in range(0, MAX_CHOICES):
            self.tally_totals(vote_choice, True, True) # Clear totals

            # Any candidate have a majority?
            for idx, candidate in enumerate(self.candidate_pool):
                if self.determine_winner(candidate):
                    end_count = True
                    break
                else:
                    print(f"No winner in round: {placement(vote_choice, 'a')}.")
                    # Remove lowest candidate
                    self.determine_loser()

            # If a winner has been determined end the counting all to together
            if end_count:
                break
    """