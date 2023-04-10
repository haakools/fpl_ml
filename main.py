"""Main script to run the tree search"""
import random
import pandas as pd
import numpy as np

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
        self.transfer_counter = 0 # how many transfer done in the given gameweek


    def query_legal_players(self, 
                            allowed_clubs: list,
                            team_budget: int,
                            allowed_positions: list,
                            n_players: int = 1, 
                            ):
        """Returns a list of legal players to transfer to"""

        print(f"Querying for {n_players} legal players")
        print(f"Allowed clubs: {allowed_clubs}")
        print(f"Allowed positions: {allowed_positions}")
        print(f"Team budget: {team_budget}")
        # This could be a function
        players_df = self.gameweek_players[
                (self.gameweek_players["team"].isin(allowed_clubs)) &
                (self.gameweek_players["cost"] <= team_budget) &
                (self.gameweek_players["position"].isin(allowed_positions))
            ].sample(n=n_players)
        return players_df # squeeze to convert to series

    def sell_player(self, team: Team):
        """Sells a random player from the team"""
        outgoing_player = random.choice(team.team_list)
        team.budget += outgoing_player.price
        team.team_list.remove(outgoing_player)
        return outgoing_player

    def buy_players(self, team: Team, players: list[Player]):
        """Buys players for the team"""
        for player in players:
            team.team_list.append(player)
            team.budget -= player.price

    def execute_transfer(self, team: Team):
        """Does a random transfer given a team"""
        # TODO: make this support multiple transfers, based on the number of transfers available
        # TODO: Make the selling and buying of players be weighted by expected points model

        # Finding out how many transfers to do
        transfers_available = team.transfers_available 
        n_transfers = np.random.binomial(transfers_available+1, 0.5)
        if n_transfers == 0:
            print("No transfers done")
            team.transfers_available = 2 # reset the transfers available
            return team

        # Sell random players
        outgoing_players = [self.sell_player(team) for _ in range(n_transfers)] 

        # Buy a random player
        allowed_clubs = team.get_allowed_clubs_for_transfer()
        allowed_positions = [outgoing.position for outgoing in outgoing_players]

        players_df = self.query_legal_players( 
            allowed_clubs,
            team.budget,
            allowed_positions,
            n_players = n_transfers,
            )
        # TODO: fix the instantiation of the player to be more failsafe
        incoming_players = [Player(player[1].squeeze(), self.gameweek) for player in players_df.iterrows()]
        self.buy_players(team, incoming_players)

        return team

def main():
    start_gw = 5
    gk_players, def_players, mid_players, fwd_players = load_all_gameweeks_players(start_gw)

    # Load all the players in their formation
    # 2GK, 5DEF, 5MID, 3FWD
    # No more than 3 players from the same team
    # Cost cannot exceed 1000    

    # Dummy team
    team_list = [
        gk_players[0],gk_players[10],
        def_players[0], def_players[15], def_players[20], def_players[30], def_players[40],
        mid_players[5], mid_players[15], mid_players[25], mid_players[35], mid_players[45],
        fwd_players[15], fwd_players[30], fwd_players[45],
    ]

    main_team = Team(
        start_gw,
        team_list,
        budget=12,
        transfers_available=1,
        )
    transfer_manager = TransferManager(start_gw)

    for gameweek in range(start_gw+1, 27):
        print(f"\nGameweek {gameweek}")
        transfer_manager.execute_transfer(main_team)
        #start_team.team_summary()
        main_team.play_out_gameweek(gameweek)

    main_team.team_summary()
if __name__ == "__main__":
    main()


