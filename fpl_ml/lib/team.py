import enum
from typing import List
import random

from fpl_ml.lib.player import Player



class Position(enum.Enum):
    """double check what the values are inside the dataset"""
    GK = 1
    DEF = 2
    MID = 3
    FWD = 4

class Team:
    """Class for handling the team and its players"""
    def __init__(
            self,
            gameweek: int,
            players: List[Player],
            budget: int,
            transfers_available: int,
            ):
        """Initialise the team with the players and budget for a given gameweek""" 
        self.gameweek = gameweek
        self.players = players
        self.budget = budget
        self.transfers_available = transfers_available

        self.chip_used = None  #

    def draw_starting_team(self):
        positions = {"GK": 1, "DEF": 3, "MID": 3, "FWD": 1}
        self.starting = [
            player for pos, min_count  in positions.items()
            for player in random.sample(
                [p for p in self.players if p.position == pos], 
                min_count
            )
        ]
        self.benched = [p for p in self.players if p not in self.starting]

    def set_captains(self):
        team = self.starting
        self.captain = team.pop(random.randrange(0,len(self.starting)))
        print(f"Setting captain to {self.captain}") 

        self.vice_captain = team.pop(random.randrange(0,len(self.starting)))
        print(f"Setting vice captain to {self.vice_captain}") 


    def get_team_info(self) -> dict:
        
        return {
            "starters": self.starting,
            "bench": self.benched,
            "captain": self.captain,
            "vice captain": self.vice_captain
        }
    
    def __repr__(self) -> str:
        return self.get_team_info()



    def set_team(self):
        self.draw_starting_team()
        self.set_captains()

        # Node information for hashing node
        self.node_information = {
            "captain": self.captain,
            "vice_captain": self.vice_captain,
            "starting": self.starting.sort(key=lambda obj: obj.id),
            "bench": self.benched.sort(key=lambda obj: obj.id),
            "chip": self.chip_used,
            "transfers_in": self.transfers_in,
            "transfers_out": self.transfers_out
        }


    def transfer(self):
        available_clubs = self.get_available_clubs_for_transfer()


    def get_available_clubs_for_transfer(self):
        return

    def get_club_count(self):
        self.club_count = {}
        for p in self.players:
            if p.team in self.club_count:
                self.club_count[p.team] += 1
            else:
                self.club_count[p.team] = 1
        return self.club_count

    def get_allowed_clubs_for_transfer(self):
        """Returns a list of clubs that can be transferred to"""
        allowed_clubs = []
        for club, count in self.get_club_count().items():
            if count < 3:
                allowed_clubs.append(club)
        return allowed_clubs


if __name__ == "__main__":
    pass