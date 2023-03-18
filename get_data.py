
"""
Want to have the data on the form of a dataframe/csv file with the following structure:
|            | PLAYER #1 | PLAYER #2 |
| GAMEWEEK 1 |           |           |
| GAMEWEEK 2 |           |           |
| GAMEWEEK 3 |           |           |
| GAMEWEEK 4 |           |           |
| GAMEWEEK 5 |           |           |
| GAMEWEEK 6 |           |           |
Could also be flipped, so that the players are the rows and the gameweeks are the columns.
"""
import requests
import pandas as pd


# PLAYER ID MAPPING

# Creating player map
def get_player_map(elements_df):
    player_map = {}
    for i in range(len(elements_df)):
        # Creating the index mappings from the LAST gameweek
        index = elements_df['id'].iloc[i]
        first_name = elements_df['first_name'].iloc[i]
        second_name = elements_df['second_name'].iloc[i]

        player_map[str(index)] = first_name + " " + second_name

    return player_map

url = "https://fantasy.premierleague.com/api/bootstrap-static/"
r = requests.get(url)
json = r.json()
for k in json.keys():
    print(k)

elements_df = pd.DataFrame(json["elements"])
elements_types_df = pd.DataFrame(json["element_types"])
teams_df = pd.DataFrame(json["teams"])
player_map = get_player_map(elements_df)


# Get the first gameweek data:
gameweek_range = range(1,28)

gameweek_stats = {}
for i in gameweek_range:
    player_stats = {}
    url = f"https://fantasy.premierleague.com/api/event/{i}/live/"
    reply = requests.get(url).json()["elements"]
    # print(len(reply)) # 573-750 players. players are only removed on new season
    for player in reply:
        player_name = player_map[str(player["id"])]
        #print(player_name)
        #print(player["stats"])
        player_stats[player_name] = player["stats"]
    gameweek_stats[str(i)] = player_stats
    # converting the dictionaries into a pandas dataframe
    df = pd.DataFrame(player_stats)
    df.to_csv(f"gameweek/gameweek_{i}.csv")