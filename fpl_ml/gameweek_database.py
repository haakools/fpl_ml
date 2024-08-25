import os
from typing import List
import json

import pandas as pd
from fpl_ml.lib.player import Player


# TODO: Make this use gameweek data from instead 
# Make a better database solution than raw csv files?
# https://github.com/vaastav/Fantasy-Premier-League.git


CURRENT_SEASON = "2024-25"
DATA_PATH = os.path.join("Fantasy-Premier-League","data")

class GameweekDatabase:
    def __init__(self, season) -> None:
        self.season = season
        self.csv_dir = f"data/season_{self.season}"
    
        self.player_id = {} #keys are season
        self.team_code_map = {}
        self.season_data = {}
        self.team_ratings = {}
        self.player_opposition = {}

    def set_season(self, season): self.season = season

    def load_player_id_list(self):
        df_id = pd.read_csv(
            os.path.join(DATA_PATH, self.season, "player_idlist.csv")
        )
        df_id['full_name'] = df_id['first_name'] + ' ' + df_id['second_name']
        self.player_id[self.season] = dict(zip(df_id['full_name'], df_id['id']))

    def load_team_ratings(self):
        df_team = pd.read_csv(
            os.path.join(DATA_PATH, self.season, "teams.csv")
        )
        self.team_code_map[self.season] = dict(zip(df_team['name'], df_team['code']))
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
        self.team_ratings[self.season]  = df_team.set_index("code")[columns].to_dict('index')

    def load_fixtures(self):
        df = pd.read_csv(
            os.path.join(DATA_PATH, self.season, "fixtures.csv")
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

    def load_season_data(self):
        df = pd.read_csv(
            os.path.join(DATA_PATH, self.season, "gws/merged_gw.csv")
        )
        df["id"] = df["name"].map(self.player_id[self.season])
        df["team_code"] = df["team"].map(self.team_code_map[self.season])
        self.season_data[self.season] = df

    def load_database(self):
        self.load_player_id_list()
        self.load_team_ratings()
        self.load_season_data()
        self.load_fixtures()

    def get_player_series(self, player_id: str):
        df = self.season_data[self.season]
        return df[df["id"] == player_id]


    def get_player_opposition(self, player_id: str, N_gameweeks:str, start_gameweek: str):
        # Get teamcode for player
        self.player_opposition[player_id] = {
            
        }
        # get 


    def get_best_players_naive(self, gameweek: int, amount_of_players: int = 20) -> List[Player]:
        df = self.season_data[season]

        players = df

