
import numpy as np
import pandas as pd
import os
import json 
import sys
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score



import matplotlib.pyplot as plt

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

    # Remove benchplayers
    df_fwd = df_fwd[df_fwd["minutes"] > 10] 

    # Trying a single player
    df_fwd = df_fwd[df_fwd["name"] == "Erling Haaland"]
    df_fwd["attack_defence_ratio"] = df_fwd["opponent_strength_defence"] / df_fwd["player_team_strength_attack"]

    # TODO: add historic playing time as a factor ?? 
    feature_columns = [
        #"opponent_strength_attack",
        "attack_defence_ratio",
        #"opponent_strength_defence",
        #"player_team_strength_attack",
        #"player_team_strength_defence",
    ]

    # Some target columns to model against
    target_columns = [
        # More fluid values
        #"expected_assists",
        "expected_goals",
        #"expected_goals_conceded",
        #"total_points",
        #"bps",

        # # Actually observed
        #"goals_conceded",
        #"goals_scored",
        #"own_goals",
        #"penalties_missed",
        #"penalties_saved",
        #"yellow_cards",
        #"red_cards",
        #"minutes",
    ]

    X = df_fwd[feature_columns].values
    y = df_fwd[target_columns[0]].values 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    # Create the plot
    output_folder = "plots"
    plt.figure(figsize=(8, 6))
    plt.scatter(X, y, alpha=0.7, c='blue', edgecolors='w', s=100)
    plt.title('Scatter Plot of "attack_defence_ratio expected_goals')
    plt.xlabel("attack_defence_ratio")
    plt.ylabel("expected_goals")

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save the plot
    plt.savefig(os.path.join(output_folder, "plot"))




    #plot_features_scatter(X_train, [0, 1], feature_columns)  


    def fit_linear_model(X_train, y_train):
        linear_model = LinearRegression()

        # Fit the model
        linear_model.fit(X_train, y_train)

        # Predict on the test set
        y_pred = linear_model.predict(X_test)

        # Evaluate the model
        print(F"Linear Model:")
        print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred)}")
        print(f"R^2 Score: {r2_score(y_test, y_pred)}")

        # Print the coefficients
        print(f"Intercept (α): {linear_model.intercept_}")
        print(f"Coefficients (β, γ): {linear_model.coef_}")

    def fit_poly_model(X_train, y_train):
        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X_train)

        # Fit the polynomial regression model
        poly_model = LinearRegression()
        poly_model.fit(X_poly, y_train)

        # Predict and evaluate
        y_pred_poly = poly_model.predict(poly.transform(X_test))

        print(F"Poly Model:")
        print(f"Mean Squared Error (Polynomial): {mean_squared_error(y_test, y_pred_poly)}")
        print(f"R^2 Score (Polynomial): {r2_score(y_test, y_pred_poly)}")


    fit_linear_model(X_train, y_train)
    fit_poly_model(X_train, y_train)

train_model("2023-24")


