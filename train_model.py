
import numpy as np
import pandas as pd
import json 
import sys
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score






from fpl_ml.lib.team import Team
from fpl_ml.lib.player import Player
from fpl_ml.fpl_api_handler import FplApiHandler, PersonalTeamInfo
from fpl_ml.gameweek_database import GameweekDatabase

def print_df(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)


def train_model(season:str):
    # All training should be on previous season data
    # Naive model should be indifferent to the rating of a player
    database = GameweekDatabase(season)
    database.load_database()

    print(f"Getting forwards")
    df_fwd = database.get_player_by_position("FWD")
    #df["opponent_team"] = df["opponent_team"].map(team_code_map)
    striker_1 = df_fwd[df_fwd["name"] == "Erling Haaland"]
    for c in striker_1.columns:
        print(c)

    feature_columns = [
        "opponent_strength_attack",
        "opponent_strength_defence",
        "player_team_strength_attack",
        "player_team_strength_defence",
    ]

    # Some target columns to model against
    target_columns = [
        # More fluid values
        "expected_assists",
        "expected_goals",
        "expected_goals_conceded",
        "total_points",
        "bps",

        # Actually observed
        "goals_conceded",
        "goals_scored",
        "own_goals",
        "penalties_missed",
        "penalties_saved",
        "yellow_cards",
        "red_cards",
        "minutes",
    ]


    X = df_fwd[feature_columns].values
    y = df_fwd["total_points"].values # the grand value


train_model("2023-24")


