"""Main script to run the tree search"""
import random
import pandas as pd


from team import Team
from player import Player

from load_players import load_all_gameweeks_players, gameweek_dict

def create_first_team(
    gk_players: list[Player],
    def_players: list[Player],
    mid_players: list[Player],
    fwd_players: list[Player],
    budget: int,
):
    """Creates a team given a set of rules
    2GK, 5DEF, 5MID, 3FWD
    No more than 3 players from the same team
    Cost cannot exceed 1000
    """

    gk_list = []
    def_list = []
    mid_list = []
    fwd_list = []


class TransferManager:
    """Class to conduct transfers and keep at 
    each node of unique combinations"""
    def __init__(self, gameweek: int):
        self.gameweek = gameweek
        self.gameweek_dict = gameweek_dict
        self.gameweek_players = gameweek_dict[gameweek] # all the players to choose from
        self.exhausted_transfers = []

    def execute_random_transfer(self, team: Team):
        """Does a random transfer given a team"""
        team_budget = team.budget

        # Sell a random player
        outgoing_player = random.choice(team.team_list) 
        # TODO: Evenutally this "random-choice" will be replaced by expected points model.
        team_budget += outgoing_player.price
        team.team_list.remove(outgoing_player)

        # Buy a random player
        allowed_clubs = team.get_allowed_clubs_for_transfer()
        incoming_player = Player(
            self.gameweek_players[
                (self.gameweek_players["team"].isin(allowed_clubs)) &
                (self.gameweek_players["cost"] <= team_budget) &
                (self.gameweek_players["position"] == outgoing_player.position)
            ].sample(n=1),
            self.gameweek,
        )

        team_budget -= incoming_player.cost
        team.team_list.append(incoming_player)
        print(f"Transferred {outgoing_player.name} to {incoming_player.name}")
        return team


def main():
    start_gw = 20
    gk_players, def_players, mid_players, fwd_players = load_all_gameweeks_players(start_gw)

    # Load all the players in their formation
    # 2GK, 5DEF, 5MID, 3FWD
    # No more than 3 players from the same team
    # Cost cannot exceed 1000    

    team_list = [
        gk_players[0],gk_players[10],
        def_players[0], def_players[15], def_players[20], def_players[30], def_players[40],
        mid_players[5], mid_players[15], mid_players[25], mid_players[35], mid_players[45],
        fwd_players[15], fwd_players[30], fwd_players[45],
    ]

    start_team = Team(
        start_gw,
        team_list,
        budget=12,
        transfers_available=1,
        )
    transfer_manager = TransferManager(start_gw)
    start_team.team_summary()

    transfer_manager.execute_random_transfer(start_team)
    start_team.team_summary()


if __name__ == "__main__":
    main()


