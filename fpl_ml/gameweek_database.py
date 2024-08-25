import os
from typing import Any

import pandas as pd
from lib.player import Player


# TODO: Make this use gameweek data from instead 
# Make a better database solution than raw csv files?
# https://github.com/vaastav/Fantasy-Premier-League.git


CURRENT_SEASON = "2024-25"
DATA_PATH = os.path.join("Fantasy-Premier-League","data")

class GameweeekDatabase:
    def __init__(self) -> None:
        self.season = CURRENT_SEASON
        self.csv_dir = f"data/season_{self.season}"
    
        self.player_id = {} #keys are season
        self.team_code_map = {}
        self.season_data = {}

    def load_player_id_list(self, season: str):
        df_id = pd.read_csv(
            os.path.join(DATA_PATH, season, "player_idlist.csv")
        )
        df_id['full_name'] = df_id['first_name'] + ' ' + df_id['second_name']
        self.player_id[season] = dict(zip(df_id['full_name'], df_id['id']))

    def load_team_id_list(self, season: str):
        df_team = pd.read_csv(
            os.path.join(DATA_PATH, season, "teams.csv")
        )

        self.team_code_map[season] = dict(zip(df_team['name'], df_team['code']))

    def load_season_data(self, season: str):
        df = pd.read_csv(
            os.path.join(DATA_PATH, season, "gws/merged_gw.csv")
        )
        df["id"] = df["name"].map(self.player_id[season])
        df["team_code"] = df["team"].map(self.team_code_map[season])
        self.season_data[season] = df

    def load_database(self, season: str):
        self.load_player_id_list(season)
        self.load_team_id_list(season)
        self.load_season_data(season)

    def get_player_series(self, player_id: str, season: str):
        df = self.season_data[season]
        return df[df["id"] == player_id]