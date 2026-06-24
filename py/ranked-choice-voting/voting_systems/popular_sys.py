# voting_systems/popular_sys.py

"""
+----------------------------------------------------------------------------
| Popular Voting System
+----------------------------------------------------------------------------
| This systerm counts only the first place votes and picks the winner by who 
| has the highest tally.
|
"""

from src.utils import get_candidate_by_uid, get_index_by_uid, show_banner
from voting_systems.base_voting_sys import BaseVotingSystem


class PopularVotingSystem(BaseVotingSystem):
    def __init__(self, candidates: list, ballots: list):
        super().__init__(candidates, ballots) 
        
        self.title = 'Popular Vote System Results'
        self.reset_candidate_pool()

    
        


    def clear_candidate_pool_totals(self):
        for candidate in self.candidate_pool:
            candidate.total = 0
            
        
    def score_ballots(self, choice: int=0):
        for ballot in self.ballots:
            print(f'ballot={ballot}')
            idx = get_index_by_uid(self.candidates, ballot[choice])
            self.candidates[idx].total += 1

    def determine_winner(self) -> bool:
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

        subtitles = []

        for candidate in self.candidates:
            line = f"Candidate: {candidate.name} | Total: {candidate.total}"
            subtitles.append(line)

        winner = get_candidate_by_uid(self.candidates, self.winner_uid)
        print(f'winning_candidate = {winner.name}')

        #line = f"Winner: {winner.name} "
        #subtitles.append(line)


        show_banner(self.title, subtitles)
        print(f"\nWinner: {winner.name} ({winner.party})")
        
    
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

   

   


    