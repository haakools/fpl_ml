import enum
from typing import List
import json
import random

from fpl_ml.lib.player import Player


MAX_TRANSFER_PER_GW = 4

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
            season_team_map: dict
            ):
        """Initialise the team with the players and budget for a given gameweek""" 
        self.gameweek = gameweek
        self.players = players
        self.budget = budget
        self.transfers_available = transfers_available
        self.season_team_map: dict = season_team_map

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
        return json.dumps(self.get_team_info(), indent=4)



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

    def get_available_clubs_for_transfer(self, transfers_out):

        team_club_counter = {team: 3 for team in self.season_team_map}
        for player in self.players:
            if player in transfers_out:
                team_club_counter[player.team_code] += 1
            else:
                team_club_counter[player.team_code] -= 1
         
        available_teams = [
            club for club in team_club_counter
            if team_club_counter.get("club", 3) < 3
        ]
        return available_teams, team_club_counter

    def get_legal_transfers(self):
        # Transfer parameters

        # just keep count when transferring instead...
        #position_requiements = {"GK": 2, "DEF": 5, "MID": 5, "FWD": 3}

        transfers_out: List[Player] = random.choices(
            self.players, 
            weights=15*[1/15],
            k=MAX_TRANSFER_PER_GW
            )
        

        for p in transfers_out:
            print(p)        

        # Get the positions that needs to be filled
        positions = [p.position for p in transfers_out] 

        available_clubs, team_club_counter = self.get_available_clubs_for_transfer(transfers_out)
        transfers_in = self.buy_players(positions, available_clubs, self.budget)

        # TODO: assertions for transfers_out, transfers_in before finalizing
        # need to ensure the transfers are unique in some sense

    def buy_players(self, positions, available_clubs, budget):
        # TODO: Make gameweek database generate expected score for all players
        all_players = []
        all_players_expected_score = []
        transfer_in = random.choices(
            all_players,
            weights=all_players_expected_score,
            k=MAX_TRANSFER_PER_GW
        )
        return transfers_in


if __name__ == "__main__":
    pass