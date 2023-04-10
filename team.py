import enum
from typing import List

from utils import load_csv
import player


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
            team_list: list[player.Player],
            budget: int,
            transfers_available: int,
            ):
        """Initialise the team with the players and budget for a given gameweek""" 
        self.gameweek = gameweek
        self.team_list = team_list
        self.budget = budget
        self.transfers_available = transfers_available

        # Team composition set at the start of the gameweek
        self.captain = None # player.Player
        self.vice_captain = None # player.Player
        self.bench = None # list of 4 players, ORDER MATTERS
        self.starting = None # list of 11 players. composition of players needs to be correct!

        # Transfer history
        self.node_information = {} # dict of gameweek: (captain, vice_captain, starting, bench)
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

    def get_position_count(self):
        self.position_count = {}
        for p in self.team_list:
            if p.position in self.position_count:
                self.position_count[p.position] += 1
            else:
                self.position_count[p.position] = 1
        return self.position_count

    def team_summary(self):
        """Prints out the team summary"""
        print("Team Summary")
        print(f"Gameweek: {self.gameweek}")
        for p in self.team_list:
            p.player_summary()

    def set_node_information(self):
        """Set the node information for the current gameweek"""
        self.node_information[self.gameweek] = (
            self.captain,
            self.vice_captain,
            self.starting,
            self.bench)

    def set_starting(self):
        """Set the starting team.
        Selecting the bench as the "worst" players in the team, and the rest
        is starting"""
        self.bench = sorted(self.team_list, key=lambda x: x.threat(), reverse=True)[11:]
        self.starting = [player for player in self.team_list if player not in self.bench]

    def set_captain_and_vice_captain(self): 
        """Only setting the captain to a player in the starting team"""
        threat_rating = [player.threat() for player in self.starting]
        self.captain = self.starting[threat_rating.index(max(threat_rating))]
        threat_rating.remove(max(threat_rating))
        self.vice_captain = self.starting[threat_rating.index(max(threat_rating))]

    def play_out_gameweek(self, gameweek: int):
        """
        Iterative function to play out the gameweek.
        1. Loads the next gameweek data
        2. Adds points to each player in the starting team. 
            If minutes played is 0, then look for substitutes 
            from the bench in the correct order.  
            If minutes played on the captain is 0, then 
            double the score for the vice captain (there are no third captain)

        After this, branch out N different scenarios for the next gameweek, i.e. states. 
        This should be 
            - transfers
            - captain changes
            - vice captain changes
            - bench changes
            - no changes 
        """
        round_points = 0
    
        if self.captain.minutes != 0:
            round_points += 2 * self.captain.player_points()
        else:
            round_points += self.vice_captain.player_points() 

        # This requires the self.bench list to be correctly ordered as wished
        subs = [player for player in self.bench if player.minutes != 0]

        for player in self.starting:
                round_points += player.player_points()
        return round_points

if __name__ == "__main__":
    pass