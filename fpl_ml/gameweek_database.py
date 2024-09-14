import os
from typing import List
import json
import sys


import pandas as pd
from fpl_ml.lib.player import Player

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

HISTORIC_VALUES = [
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
            'fixture', # not needed (?)
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
TEAM_RATINGS_COLUMNS = [
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
        print(f"GameweekDatabase:: Player ids loaded")

    def load_team_ratings(self):
        df_team = pd.read_csv(
            os.path.join(DATA_PATH, self.season, "teams.csv")
        )
        self.teamname_code_map[self.season] = dict(zip(df_team['name'], df_team['code']))
        self.team_code_map[self.season] = dict(zip(df_team['id'], df_team['code']))
        self.team_ratings[self.season]  = df_team.set_index("code")[TEAM_RATINGS_COLUMNS].to_dict('index')
        #self.team_ratings[self.season]

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
        print(f"GameweekDatabase:: team fixtures loaded")

    def load_season_data(self):
        """
        Loading merged gameweek data for players per gameweek 
        Parsing:
            team ids to be indexable across different season
            Adding opponent 
            Adding opponent info (strength(s), name, etc)
        Does NOT append future gameweeks if there are less than 38 for a player TODO 
        """
        df = pd.read_csv(
            os.path.join(DATA_PATH, self.season, "gws/merged_gw.csv")
        )
        # Evidently merged_gw has two different names, e.g. "Đorđe Petrović" and "Djordje Petrovic".
        #"Đorđe Petrović" and "Djordje Petrovic"
        # petrovic_nonascii =  df[(df["position"]=="GK") & (df["name"] == "Đorđe Petrović")]
        # print(len(petrovic_nonascii))
        # petrovic_ascii =  df[(df["position"]=="GK") & (df["name"] == "Djordje Petrovic")]
        # print(len(petrovic_nonascii))
        # TODO: Fix this with adding both the player in the map, as this is defined in the merged_gw.
        # Seems to update manually

        # Dropping (for now) non-necesseary information
        drop_columns = [
            "transfers_balance",
            "transfers_in",
            "transfers_out",
            "selected",
            "kickoff_time",
            "fixture", # some fixture id, idk if useful
            "xP",  # this is some precomputed stuff that is not useful
        ]
        df = df.drop(columns=drop_columns)


        df["id"] = df["name"].map(self.player_id[self.season])
        df["team_code"] = df["team"].map(self.teamname_code_map[self.season])

        # Create team lookup map from players
        nan_rows = df[df['id'].isna()]
        nan_names = nan_rows["name"].unique()
        print(f"[WARNING] GameweekDatabase found {len(nan_rows)} NaNs for players: {nan_names}")
        df_unique = df.drop_duplicates(subset='id')
        df_unique = df_unique.copy()  # Make an explicit copy
        df_unique.loc[:, "id"] = df_unique["id"].fillna(-1).astype(int)

        # this maps inter season player_id 1.2..N to a team 
        self.player_team_map[self.season] = df_unique.drop_duplicates(
             subset='id').groupby('id')['team_code'].apply(list).to_dict()

        # Converting opponent_team to inter-season teamcode
        df.opponent_team = df.opponent_team.astype(int)
        df["opponent_team"] = df["opponent_team"].map(self.team_code_map[self.season])



        # TODO: Make this horrible ChatGPT code more readable 
        def add_team_prefix_to_team_info(team_info, prefix: str):
            team_data = []
            for team_id, team_stats in team_info.items():
                prefixed_stats = {f'{prefix}{key}': value for key, value in team_stats.items()}
                if prefix == "opponent_":
                    prefixed_stats['opponent_team'] = team_id
                else:
                    prefixed_stats['team_code'] = team_id
                team_data.append(prefixed_stats)
            return pd.DataFrame(team_data)

        # Assuming self.team_ratings[self.season] is a dictionary of team ratings
        opponent_team_info_df = add_team_prefix_to_team_info(self.team_ratings[self.season], "opponent_")
        player_team_info_df = add_team_prefix_to_team_info(self.team_ratings[self.season], "player_team_")

        # Merge the dataframes
        df = df.merge(opponent_team_info_df, how='left', on='opponent_team')
        df = df.merge(player_team_info_df, how='left', on='team_code')

        # Apply the home/away logic
        df['opponent_strength_attack'] = df.apply(lambda row: row['opponent_strength_attack_home'] if not row['was_home'] else row['opponent_strength_attack_away'], axis=1)
        df['opponent_strength_defence'] = df.apply(lambda row: row['opponent_strength_defence_home'] if not row['was_home'] else row['opponent_strength_defence_away'], axis=1)
        df['player_team_strength_attack'] = df.apply(lambda row: row['player_team_strength_attack_home'] if row['was_home'] else row['player_team_strength_attack_away'], axis=1)
        df['player_team_strength_defence'] = df.apply(lambda row: row['player_team_strength_defence_home'] if row['was_home'] else row['player_team_strength_defence_away'], axis=1)

        # Drop the unnecessary columns
        columns_to_drop = [ c for c in df.columns if c.endswith("_away") or c.endswith("_home")]
        df = df.drop(columns=columns_to_drop)

        self.season_data[self.season] = df
        print(f"GameweekDatabase:: team fixtures loaded")

    def generate_player_fixture_list(self, gameweek:int):
        """Creating future fixture list"""
        self.player_fixture_list = {}        
        player_folder_path = os.path.join(DATA_PATH, self.season, "players")

        # Values for gameweeks already played
        for player_folder in os.listdir(player_folder_path):
            df = pd.read_csv(
                os.path.join(player_folder_path, player_folder, "gw.csv")
            )
            print(f"Parsing: {player_folder}")
            player_id = player_folder.split("_")[-1]
            fixture_list = []
            # Get team of the player 
            for gw, player in df[HISTORIC_VALUES].iterrows(): # played gameweeks loop
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
            self.player_fixture_list[player_id] = fixture_list
            #print(json.dumps(self.player_fixture_list, indent=4))
        return self.player_fixture_list

    def get_player_series(self, player_id: str):
        df = self.season_data[self.season]
        return df[df["id"] == player_id]

    def get_player_by_position(self, position: str):
        df = self.season_data[self.season]
        return df[df["position"] == position]

    # Expected points model below
    def get_player_opposition(self, player_id: str, N_gameweeks:str, start_gameweek: str):
        # Get teamcode for player
        self.player_opposition[player_id] = {
        }


    def get_best_players_naive(self, gameweek: int, amount_of_players: int = 20) -> List[Player]:
        pass
        #df = self.season_data[season]

        #players = df

