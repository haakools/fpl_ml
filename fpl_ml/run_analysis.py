"""Main entry to analyze team"""
import json

from fpl_ml.lib.team import Team
from fpl_ml.lib.player import Player
from fpl_ml.fpl_api_handler import FplApiHandler, PersonalTeamInfo
from fpl_ml.gameweek_database import GameweekDatabase
from fpl_ml.mcts import MCTS, MCTSNode


def populate_team(team_info: PersonalTeamInfo, season: str, database: GameweekDatabase) -> Team:


    player_list = [
        Player(player_id, database.get_player_series(player_id), team_info.gameweek)
        for player_id in team_info.player_ids()
    ]
    return Team(
        team_info.gameweek,
        player_list,
        team_info.budget, 
        team_info.available_transfers,
        database.team_code_map[season]
        ) 

def run_analysis(season:str, team_id: int, max_depth: int, iterations: int, output_file: bool, verbose: bool):
    if not isinstance(team_id, int):
        team_id = int(team_id)
    fpl_api = FplApiHandler()

    database = GameweekDatabase(season)
    database.load_database()

    personal_team_info: PersonalTeamInfo = fpl_api.get_personal_team_info(team_id)

    print(f"Personal team info {personal_team_info}")


    # Root Node
    team: Team = populate_team(
        personal_team_info,
        season,
        database=database
        )

    print("Selected team:")
    for player in team.players:
        print(player)
    import sys
    sys.exit(0)

    mcts = MCTS(team, database, max_depth=max_depth, iterations=iterations)
    result = mcts.search()

    print(result)
