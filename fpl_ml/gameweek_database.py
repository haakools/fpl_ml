import os
from typing import List
import json

import pandas as pd
from lib.player import Player


# TODO: Make this use gameweek data from instead 
# Make a better database solution than raw csv files?
# https://github.com/vaastav/Fantasy-Premier-League.git


CURRENT_SEASON = "2024-25"
DATA_PATH = os.path.join("Fantasy-Premier-League","data")

class GameweekDatabase:
    def __init__(self) -> None:
        self.season = CURRENT_SEASON
        self.csv_dir = f"data/season_{self.season}"
    
        self.player_id = {} #keys are season
        self.team_code_map = {}
        self.season_data = {}
        self.team_ratings = {}


    def load_player_id_list(self, season: str):
        df_id = pd.read_csv(
            os.path.join(DATA_PATH, season, "player_idlist.csv")
        )
        df_id['full_name'] = df_id['first_name'] + ' ' + df_id['second_name']
        self.player_id[season] = dict(zip(df_id['full_name'], df_id['id']))

    def load_team_ratings(self, season: str):
        df_team = pd.read_csv(
            os.path.join(DATA_PATH, season, "teams.csv")
        )
        self.team_code_map[season] = dict(zip(df_team['name'], df_team['code']))
        columns = [
            #"code",
            "name",
            "short_name",
            "strength",
            "strength_overall_home",
            "strength_overall_away",
            "strength_attack_home", 
            "strength_attack_away", 
            "strength_defence_home",
            "strength_defence_away",
        ]
        self.team_ratings[season]  = df_team.set_index("code")[columns].to_dict('index')

    def load_fixtures(self, season: str):
        df = pd.read_csv(
            os.path.join(DATA_PATH, season, "fixtures.csv")
        )
        home_games = df[['team_h', 'team_a', 'event']].rename(columns={'team_h': 'team', 'team_a': 'opponent'})
        home_games['home'] = True

        away_games = df[['team_a', 'team_h', 'event']].rename(columns={'team_a': 'team', 'team_h': 'opponent'})
        away_games['home'] = False

        all_games = pd.concat([home_games, away_games], ignore_index=True)
        self.team_map = {
            team: {
                row['event']: {'opponent': row['opponent'], 'home': row['home']}
                for _, row in group.iterrows()
            }
            for team, group in all_games.groupby('team')
        }

        print(json.dumps(self.team_map, indent=4))

    def load_season_data(self, season: str):
        df = pd.read_csv(
            os.path.join(DATA_PATH, season, "gws/merged_gw.csv")
        )
        df["id"] = df["name"].map(self.player_id[season])
        df["team_code"] = df["team"].map(self.team_code_map[season])
        self.season_data[season] = df

    def load_database(self, season: str):
        self.load_player_id_list(season)
        self.load_team_ratings(season)
        self.load_season_data(season)
        self.load_fixtures(season)

    def get_player_series(self, player_id: str, season: str):
        df = self.season_data[season]
        return df[df["id"] == player_id]

    def get_best_players_naive(self, season: str, gameweek: int, amount_of_players: int = 20) -> List[Player]:
        # The expected points needs to be calculated
        df = self.season_data[season]

        players = df

