"""Main entry to analyze team"""


from lib.team import Team
from lib.player import Player
from gameweek_database import GameweeekDatabase

# 1. Initalize the gameweek database with all available players


database = GameweeekDatabase()




# 1. Enter your current players 
# / your teams identifier and then parse the team information

TEAM_ID = "2180411"

def get_entry_data(entry_id: str) -> dict:
    import requests
    endpoint = f"https://fantasy.premierleague.com/api/entry/{entry_id}/history"
    response: requests.Response = requests.get(endpoint)
    if response.ok:
        if response.stauts_code == 200: return response.json() 




summary = get_entry_data(TEAM_ID)
#personal_data = get_entry_personal_data(team_id)


gameweek = 1
budget = 1
transfers_available = 1


# 2. Populate the team with the players

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









