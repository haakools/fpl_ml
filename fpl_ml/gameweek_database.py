import os
from typing import List
import json
import sys


import pandas as pd
from fpl_ml.lib.player import Player
from fpl_ml.lib.expected_points import ExpectedPointsModel

# TODO: Make this use gameweek data from instead 
# Make a better database solution than raw csv files?
# https://github.com/vaastav/Fantasy-Premier-League.git



# TODO: actually make a database instead of this ugly lookup table pandas mess

# PSA: FPL runs with different IDs between seasons. Teamcodes are AFAIK constant over all seasons, meanwhile
# they create 1-20 ids for teams during seasons aswell.
#  Some endpoint does give interseason-teamcodes, some give intraseason-teamcodes, some give freetext name for
# clubs.
# Players seem to have their index values reset at each season aswell.


CURRENT_SEASON = "2024-25"
DATA_PATH = os.path.join("Fantasy-Premier-League","data")

class GameweekDatabase:
    def __init__(self, season) -> None:
        self.season = season
        self.csv_dir = f"data/season_{self.season}"
    
        self.player_id = {} #keys are season
        self.season_data = {}
        self.player_opposition = {}
        self.team_code_map = {}
        self.teamname_code_map = {}
        self.team_ratings = {}
        self.team_fixtures = {}
        self.player_team_map = {}

    def load_database(self):
        self.load_player_id_list()
        self.load_team_ratings()
        self.load_season_data()
        self.load_fixtures()
        self.load_team_ratings()

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
        self.teamname_code_map[self.season] = dict(zip(df_team['name'], df_team['code']))
        self.team_code_map[self.season] = dict(zip(df_team['id'], df_team['code']))
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

        season_teamcode_map = self.team_code_map[self.season]
        self.team_fixtures[self.season] = {
            season_teamcode_map[int(team)]: {
                row['event']: {
                    'opponent': season_teamcode_map[int(row['opponent'])],
                    'home': row['home']}
                for _, row in group.iterrows()
            }
            for team, group in all_games.groupby('team')
        }

    def load_season_data(self):
        df = pd.read_csv(
            os.path.join(DATA_PATH, self.season, "gws/merged_gw.csv")
        )
        df["id"] = df["name"].map(self.player_id[self.season])
        df["team_code"] = df["team"].map(self.teamname_code_map[self.season])
    

        self.season_data[self.season] = df


        # Create team lookup map from players
        nan_rows = df[df['id'].isna()]
        print(nan_rows)
        sys.exit(0)

        df_unique = df.drop_duplicates(subset='id')
        print(df_unique["id"].to_list())
        df_unique["id"] = df_unique["id"].astype(int)

        self.player_team_map[self.season] = df_unique.drop_duplicates(
             subset='id').groupby('id')['team_code'].apply(list).to_dict()

        print(json.dumps(self.player_team_map[self.season], indent=4))

        sys.exit(0)


    def generate_player_fixture_list(self, gameweek:int):
        self.player_fixture_list = {}        
        import sys
        player_folder_path = os.path.join(DATA_PATH, self.season, "players")

        # Values for gameweeks already played
        historic_values = [
            'assists',
            'bonus',
            'bps',
            'clean_sheets',
            'creativity',
            'element',
            'expected_assists',
            'expected_goal_involvements',
            'expected_goals',
            'expected_goals_conceded',
            #'fixture',
            'goals_conceded',
            'goals_scored',
            'ict_index',
            'influence',
            'minutes',
            'opponent_team',
            'own_goals',
            'penalties_missed',
            'penalties_saved',
            'red_cards',
            'round', #gameweek
            'saves',
            'starts',
            'team_a_score',
            'team_h_score',
            'threat',
            'total_points',
            'value',
            'was_home',
            'yellow_cards'
            ]

        for player_folder in os.listdir(player_folder_path):
            df = pd.read_csv(
                os.path.join(player_folder_path, player_folder, "gw.csv")
            )
            print(f"Parsing: {player_folder}")
            player_id = player_folder.split("_")[-1]
            fixture_list = []
            # Get team of the player 



            sys.exit(0)


            for gw, player in df[historic_values].iterrows(): # played gameweeks loop
                iter_gw = gw+1
                if iter_gw < gameweek:
                    fixture_list.append(
                        {
                            **player.to_dict(),
                            "opponent_team_code": self.team_code_map[self.season][player.opponent_team],
                        }
                    )
                else:
                    fixture_list.append(
                        {
                            "name": player.name,
                            "oppnonent": "TBD"
                        })
            # Loop over future fixtures

            self.player_fixture_list[player_id] = fixture_list
            print(json.dumps(self.player_fixture_list, indent=4))
            sys.exit(0)
        return self.player_fixture_list



    def get_player_series(self, player_id: str):
        df = self.season_data[self.season]
        return df[df["id"] == player_id]


    # Expected points model below
    def get_player_opposition(self, player_id: str, N_gameweeks:str, start_gameweek: str):
        # Get teamcode for player
        self.player_opposition[player_id] = {
                        
        }
        # get 


    def get_best_players_naive(self, gameweek: int, amount_of_players: int = 20) -> List[Player]:
        df = self.season_data[season]

        players = df

