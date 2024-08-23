"""Main entry to analyze team"""
from lib.team import Team
from lib.player import Player
from gameweek_database import GameweeekDatabase

# 1. Initalize the gameweek database with all available players


database = GameweeekDatabase()




# 1. Enter your current players 
# / your teams identifier and then parse the team information


# Todo: make this player IDs when selecting team
player_ids = [
    ("Martinez",
    ("Saliba",
    ("Burn",
    ("Pedro Porro",
    ("Andersen",
    ("Palmer",
    ("Ødegaard",
    ("Saka",
    ("Longstaff",
    ("Watkins",
    ("Isak",
    ("Flekken",
    ("Chilwell",
    ("Toney",
    ("Smith Rowe"
]



# 2. Populate the team with the players

def populate_team(player_ids: list) -> Team:

    player_list: list[Player] = [
        database.create_player(player_id)
        for player_id in player_ids
    ]
    return Team(player_list) 


team: Team = populate_team(player_ids)



# 3. Iterate over different branches









