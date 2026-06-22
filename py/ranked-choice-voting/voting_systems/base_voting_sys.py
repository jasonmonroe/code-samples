# voting_systems/.py

"""
+----------------------------------------------------------------------------
| Base Voting System
+----------------------------------------------------------------------------
| Parent abstract class for all voting systems.  

"""

from abc import ABC, abstractmethod

class VotingSystem(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def determine_winner():
        pass