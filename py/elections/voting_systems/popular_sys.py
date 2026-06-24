# voting_systems/popular_sys.py

"""
+----------------------------------------------------------------------------
| POPULAR VOTING SYSTEM
+----------------------------------------------------------------------------
| This systerm counts only the first place votes and picks the winner by whom 
| has the highest tally. No majority needed. Only one around.  
|
| Note: If there's a tie, remove the least voted candidate, reset the total 
| and count {next place} votes to pick winner. 

| => or do not remove a candidate
| and just count the next vote of the two remaining candidates?
|
+----------------------------------------------------------------------------
"""

import logging
from uuid import MAX
from src.constants import FIRST_CHOICE, I_RIBBON, MAX_CHOICES
from src.utils import get_candidate_by_uid, get_index_by_uid, placement, show_banner
from voting_systems.base_voting_sys import BaseVotingSystem


class PopularVotingSystem(BaseVotingSystem):
    def __init__(self, candidates: list, ballots: list):
        super().__init__(candidates, ballots) 
        
        self.title = "Popular Vote" + self.title
        #self.reset_candidate_pool()

    


    
        


    #def clear_candidate_pool_totals(self):
        #for candidate in self.candidate_pool:
        #    candidate.total = 0
            
        
    #def score_ballots(self, choice: int=0):
    #    for ballot in self.ballots:
    #        print(f'ballot={ballot}')
    #        idx = get_index_by_uid(self.candidates, ballot[choice])
    #        self.candidates[idx].total += 1


    def determine_winner_fast(self):

        candidates = self.candidate_pool
        choice = FIRST_CHOICE

        #is_winner = False
        while choice < MAX_CHOICES:
            print(f"{placement(choice, 'a').title()} round.")
            highest_total = 0
            winners = []
            
            # Check which candidate has the highest vote
            for candidate in candidates:
                

                if candidate.votes[choice] > highest_total:
                    highest_total = candidate.votes[choice]
                    #highest_total_cnt += 1
                    winners = [candidate]
                elif candidate.votes[choice] == highest_total:
                    #highest_total_cnt += 1
                    winners.append(candidate)
                else:
                    # remove candidate
                    pass


            if len(winners) == 0:
                logging.error("There is no one in the lead after the first round.  Check data.")

            # Has anyone won?
            if len(winners) == 1:
                #is_winner = True
                logging.info("Success! We have a winner.")
                self.winner = winners[0]
                break
            else:
                # We have multiple leaders so lets go to second round.  Update the candidates by the "pool of winners."
                logging.info(f"No winner after {placement(choice, 'a')} round.  Limiting pool to {winners}.")
                candidates = winners
                
            # Go to next choice
            choice += 1
            logging.debug(f"Updating round to {choice}.")
            

        # Loop Breaks
        print('LOOP DONE')



            

    def determine_winner_quick(self):

       
        candidates = self.candidate_pool
        choice = FIRST_CHOICE

        highest_total = max(candidate.total for candidate in candidates)
        winners = [candidate for candidate in candidates if candidate.total == highest_total]

        while (len(winners) > 1 and choice < MAX_CHOICES):

            if len(winners) == 1:
                print(f'Winner: {winners}')
                self.winner = winners[0]
                break
                
            else:

                # If for the small chance there is a tie, clear totals, count ballots again with next choice
                choice += 1
                self.tally_ballots(choice, True, True)

                highest_total = max(candidate.total for candidate in candidates)
                winners = [candidate for candidate in candidates if candidate.total == highest_total]
            
        # Loop complete
        print(f'LOOP COMPLETE')




        


    def determine_winner(self):

        # Copy candidate remove from the pool.
        candidates = self.candidate_pool

        choice = FIRST_CHOICE
        itr = 0
        is_tie = False
        highest_total, highest_total_ctr = 0, 0
      
        while len(candidates) > 1 and choice < MAX_CHOICES:
            loser_candidate = None

            for idx, candidate in enumerate(candidates):

                if candidate.total > highest_total:
                    highest_total = candidate.total
                
                else:
                    print(f'Not the highest.  Loser candidate {idx}.')
                    loser_candidate = candidate
                    loser_candidate_idx = idx
                    #candidates.pop(idx)





            if loser_candidate is not None:
                print(f'Removing (idx={loser_candidate_idx}),  {loser_candidate.uid} from the candidate pool.')
                candidates.pop(loser_candidate_idx)

            
            itr += 1


        # Loop complete
        print(f'LOOP COMPLETE')

        self.winner = candidates




    def determine_winner2(self):

        # copy candidate remove from the pool
        candidates = self.candidates.copy() 

        itr = 0
        while self.candidate_pool.length > 1 and itr < 20:

            loser_candidate = None

    
            highest_idx, highest_total, highest_cnt = 0, 0, 1
            for idx, candidate in enumerate(self.candidate_pool.pool):
                if candidate.total >= highest_total:
                    pass






            if loser_candidate is not None:
                print(f'Removing {loser_candidate.uid} from the candidate pool.')
            self.candidate_pool.remove(loser_candidate)

            # Prevent run-time error
            print(f'itr = {itr}')
            itr += 1
        

    def determine_winner_old(self) -> bool:
        # Simply get the candidate with the highest count.  If there is a tie pull them all into the candidate pool and vote by next choice.
        #highest = [0, 0, 1] # index, total, cnt
        highest = [0, 0, 1]
        vote_ctr = []
        """
        for i, candidate in enumerate(self.candidates):
            #highest_qty = 0
            print(f'\nDEBUG: {candidate.total} >= {highest[1]}')
            if candidate.total >= highest[1]:
                highest[0] = i
                vote_ctr.append(candidate.total)
                self.add_to_candidate_pool(candidate.uid)
               
                #highest_qty += 1
                print(f'DEBUG ?: {candidate.total} == {highest[1]}')
                if candidate.total == highest[1]:
                    
                    highest[2] += 1
                    print(f'Yes, inc ctr. highest[2] = {highest[2]}')
                
                highest[1] = candidate.total
                #self.vote_cnts = {'idx'}
            else:
                print(f'{candidate.total} not the highest ')
        """
        itr = 0

        highest_total = 0
        highest_ctr = 0
        idx = 0

        while len(self.candidate_pool) > 1 and itr < 15:
            print(f'while() -> candidate_pool={self.candidate_pool}')
            
            # Track the absolute loser of this round
            loser_candidate = None  
            
            for i, candidate in enumerate(self.candidate_pool):
                print(f'\nDEBUG: {candidate.total} >= {highest[1]}')
                
                if candidate.total >= highest[1]:
                    #idx - i
                    highest[0] = i
                    highest[1] = candidate.total
                elif candidate.total == highest[1]:
                    highest[2] += 1
                    print(f'candidate.total == {highest[1]}:')
                    print("Is there a tie?")

                    # Is there a tie
                    if highest[2] >= 2:
                        print('We might have a tie.  Break it')

                else:
                    print(f'{candidate.total} not the highest. ')
                    # Instead of deleting immediately, save a reference to the loser
                    loser_candidate = candidate 

            # REMOVE SAFELY OUTSIDE THE FOR-LOOP
            if loser_candidate is not None:
                print(f'Removing {loser_candidate.uid} from the candidate pool.')
                self.remove_loser(loser_candidate) # This parent call works perfectly here

            # Do we have a tie?


            itr += 1

        
        """
        while len(self.candidate_pool) > 1 and itr < 100:
            print(f'while() -> candidate_pool={self.candidate_pool}')
            for i, candidate in enumerate(self.candidate_pool):
                #highest_qty = 0

                print(f'\nDEBUG: {candidate.total} >= {highest[1]}')
                if candidate.total >= highest[1]:
                    highest[0] = i
                    
                    #vote_ctr.append(candidate.total)
                    #self.add_to_candidate_pool(candidate.uid)
                
                    #highest_qty += 1
                    print(f'DEBUG ?: {candidate.total} == {highest[1]}')
                    #if candidate.total == highest[1]:
                        
                        #highest[2] += 1
                        
                    #highest[2] += 1
                    highest[1] = candidate.total
                    #self.vote_cnts = {'idx'}
                elif candidate.total == highest[1]:
                    print(f'Yes, inc ctr. highest[2] = {highest[2]}')
                    highest[2] += 1
                else:
                    print(f'{candidate.total} not the highest ')
                    print(f'Removing {candidate.uid} from the candidate pool.')
                    #self.remove_from_candidate_pool(candidate)
                    self.remove_loser(candidate)

            itr += 1
        """

        print(f'highest={highest}')
        # Check for tie
        print(f'remaing in pool={self.candidate_pool}')

        

        if self.check_tie(highest[2]):
            self
        else:
            # No tie

            winning_index = highest[0]
            self.winner_uid = self.candidates[winning_index].uid
            print(f'Winning UID: {self.winner_uid}\n')

            return True
        
        return False

    

    def show_results(self):

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
            
    
    
    def check_tie(self, tied_candidate_cnt):
        # Are there any other candidates with
        return tied_candidate_cnt > 1

 
       
    def break_tie(self, choice: int):
        # Call recursively
        # return [max(candidates, key=lambda c: c.total)]
        #self.clear_candidate_pool_totals()
        next_choice = choice + 1
        self.score_ballots(next_choice)

        # total should be updated by now
        for candidate in self.candidate_pool:
            pass



    def break_tie2(self, highest_vote_cnt: int, choice: int):
        # Get all candidates that have this vote count and put them in the pool
        # Get all candidates that have this vote count and put them in the pool
        # Get all candidates that have this vote count and put them in the pool
        for candidate in self.candidate_pool:
            if candidate.total < highest_vote_cnt:
                self.remove_from_candidate_pool(candidate)
            
        # Now look at t

    def determine_loser():
        pass

   

   


    