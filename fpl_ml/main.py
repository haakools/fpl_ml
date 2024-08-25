"""Main entry to analyze team"""
import json

from lib.team import Team
from lib.player import Player
from fpl_ml.fpl_api_handler import FplApiHandler, PersonalTeamInfo
from gameweek_database import GameweekDatabase
from fpl_ml.mcts import MCTS, MCTSNode


def populate_team(team_info: PersonalTeamInfo, season: str, database: GameweekDatabase) -> Team:


    player_list = [
        Player(player_id, database.get_player_series(player_id, SEASON), team_info.gameweek)
        for player_id in team_info.player_ids()
    ]
    return Team(
        team_info.gameweek,
        player_list,
        team_info.budget, 
        team_info.available_transfers,
        database.team_code_map[SEASON]
        ) 


fpl_api = FplApiHandler()

TEAM_ID = "2180411"
SEASON = "2023-24"

database = GameweekDatabase()
database.load_database(SEASON)
team_info: PersonalTeamInfo = fpl_api.get_personal_team_info(TEAM_ID)


# Root Node
team: Team = populate_team(team_info, SEASON, database=database)

print("Selected team:")
for player in team.players:
    print(player)


mcts = MCTS(team, database, max_depth=1, iterations=2)
result = mcts.search()

print(result)

