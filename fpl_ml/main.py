"""Main entry to analyze team"""
import json

from lib.team import Team
from lib.player import Player
from fpl_ml.fpl_api_handler import FplApiHandler
from gameweek_database import GameweeekDatabase

# 1. Initalize the gameweek database with all available players


database = GameweeekDatabase()

# 1. Enter your current players 
# / your teams identifier and then parse the team information

TEAM_ID = "2180411"

fpl_api = FplApiHandler()
summary = fpl_api.get_entry_data(TEAM_ID)
#print(json.dumps(summary, indent=4))

chips_used: list = summary.get("chips")
gameweek = len(summary.get("current"))+1
budget = [
    e.get("bank") 
    for e in summary.get("current", []) 
    if e.get("event") == gameweek
    ]
# TODO: get transfer available
transfers_available = 1

print(f"""
    TEAM_ID {TEAM_ID}
    Chips used {chips_used}
    Starting at gameweek {gameweek}
    Current Budget: {budget}
""")

#personal_data = fpl_api.get_personal_entry_data(TEAM_ID)
#print(json.dumps(personal_data, indent=4))

gameweek_data = fpl_api.get_gameweek_data(TEAM_ID, gameweek)
print(json.dumps(gameweek_data, indent=4))


# 2. Populate the team with the players (ROOT Node)

def populate_team(player_ids: list) -> Team:

    player_list = [
        database.create_player(player_id)
        for player_id in player_ids
    ]
    return Team(
        gameweek,
        player_list,
        budget, 
        transfers_available
        ) 

#team: Team = populate_team(player_ids)



# 3. Iterate over different branches









