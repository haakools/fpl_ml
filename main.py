"""Main script to run the tree search"""

from team import Team
from player import Player


from load_players import load_all_gameweeks_players

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



def main():
    start_gw = 20
    gk_players, def_players, mid_players, fwd_players = load_all_gameweeks_players(start_gw)

    # Load all the players in their formation
    # 2GK, 5DEF, 5MID, 3FWD
    # No more than 3 players from the same team
    # Cost cannot exceed 1000    

    start_team = Team(
        start_gw,
        [gk_players[0],gk_players[10]],
        [def_players[0], def_players[15], def_players[20], def_players[30], def_players[40]],
        [mid_players[5], mid_players[15], mid_players[25], mid_players[35], mid_players[45]],
        [fwd_players[15], fwd_players[30], fwd_players[45]],
        12
        )

    start_team.team_summary()

# Need a way to create a team following the rules
if __name__ == "__main__":
    main()


