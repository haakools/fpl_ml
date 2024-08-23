import enum
from typing import List
import random

from player import Player



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
            team_list: List[Player],
            budget: int,
            transfers_available: int,
            ):
        """Initialise the team with the players and budget for a given gameweek""" 
        self.gameweek = gameweek
        self.team_list = team_list
        self.budget = budget
        self.transfers_available = transfers_available

    def draw_starting_team(self):
        positions = {"GK": 1, "DEF": 3, "MID": 3, "FWD": 1}
        self.starting = [
            player for pos, min_count  in positions.items()
            for player in random.sample(
                [p for p in self.team_list if p.position == pos], 
                min_count
            )
        ]
        self.benched = [p for p in self.team_list if p not in self.starting]

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


    def set_team(self):
        self.draw_starting_team()
        self.set_captains()

        # Transfer history
        self.node_information = {
           
        } # dict of gameweek: (captain, vice_captain, starting, bench)
        self.transfers = {} # dict of gameweek: list of tuples of (player.Player, player.Player)

    def get_club_count(self):
        self.club_count = {}
        for p in self.team_list:
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