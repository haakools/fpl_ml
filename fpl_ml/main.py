"""Main entry to analyze team"""
import json

from lib.team import Team
from lib.player import Player
from fpl_ml.fpl_api_handler import FplApiHandler, PersonalTeamInfo
from gameweek_database import GameweeekDatabase


def populate_team(team_info: PersonalTeamInfo, database: GameweeekDatabase) -> Team:

    player_list = [
        database.create_player(player_id)
        for player_id in team_info.player_ids()
    ]
    return Team(
        team_info.gameweek,
        player_list,
        team_info.budget, 
        team_info.available_transfers
        ) 

database = GameweeekDatabase()
database.load_database()

fpl_api = FplApiHandler()

TEAM_ID = "2180411"
team_info: PersonalTeamInfo = fpl_api.get_personal_team_info(TEAM_ID)


# Root Node
team: Team = populate_team(team_info, database=database)


# 3. Iterate over different branches





