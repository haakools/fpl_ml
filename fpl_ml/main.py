"""Main entry to analyze team"""
import json

from lib.team import Team
from lib.player import Player
from fpl_ml.fpl_api_handler import FplApiHandler, PersonalTeamInfo
from gameweek_database import GameweeekDatabase


def populate_team(team_info: PersonalTeamInfo, season: str, database: GameweeekDatabase) -> Team:


    player_list = [
        Player(player_id, database.get_player_series(player_id, SEASON), team_info.gameweek)
        for player_id in team_info.player_ids()
    ]
    return Team(
        team_info.gameweek,
        player_list,
        team_info.budget, 
        team_info.available_transfers
        ) 





fpl_api = FplApiHandler()

TEAM_ID = "2180411"
SEASON = "2023-24"

database = GameweeekDatabase()
database.load_database(SEASON)
team_info: PersonalTeamInfo = fpl_api.get_personal_team_info(TEAM_ID)


# Root Node
team: Team = populate_team(team_info, SEASON, database=database)


for player in team.players:
    print(player)
    player.print_json()
    import sys
    sys.exit(0)
# 3. Iterate over different branches





