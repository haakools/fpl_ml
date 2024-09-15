
import os
import json 
import sys

import optuna
import xgboost as xgb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, KFold

from fpl_ml.gameweek_database import GameweekDatabase
from plotting_utils import (
    plot_and_save,
    plot_crossplot,
    plot_feature_importance
)


# TRAINING VALUES
N_TRIALS = 500  # how many optuna trials for XGBOOST
N_GAMES_AVERAGE = 2 # how many previous matches to calculate form


def print_df(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)


def load_and_preprocess_season_data(season):
    database = GameweekDatabase(season)
    database.load_database()
    print("Loading data for expected-expected goals model")

    df = database.get_player_by_position(["DEF", "MID", "FWD"])
    #df = df[df["minutes"] >= 60]

    df["attack_defence_ratio"] = df["opponent_strength_defence"] / df["player_team_strength_attack"]
    df = df.sort_values(['name', 'GW'])


    # Moving average FPL derived statistics
    columns_to_average = ['ict_index', 'influence', 'creativity', 'threat']

    def moving_average(group, col, N=6):
        return group[col].rolling(window=N, min_periods=1).mean()


    for col in columns_to_average:
        df[f'{col}_avg'] = df.groupby('name').apply(
            lambda x: moving_average(x, col, N_GAMES_AVERAGE)
        ).reset_index(level=0, drop=True).shift(1).fillna(0)

    for col in columns_to_average:
        max_val = df[f'{col}_avg'].max()
        min_val = df[f'{col}_avg'].min()
        df[f'{col}_normalized_avg'] = (df[f'{col}_avg'] - min_val) / (max_val - min_val)

    # Moving average expected goals
    df["expected_goals_per_minute"] = df["expected_goals"] / df["minutes"]
    df["expected_goals_per_minute"] = df["expected_goals_per_minute"].fillna(0)

    df['expected_goals_avg'] = df.groupby('name').apply(
        lambda x: x['expected_goals'].rolling(window=N_GAMES_AVERAGE, min_periods=1).mean()
    ).reset_index(level=0, drop=True).shift(1).fillna(0)
    return df


def train_model(season:str):
    seasons = [
        #"2021-22",
        "2022-23",
        "2023-24"
    ]

    df = pd.concat([load_and_preprocess_season_data(season) for season in seasons], ignore_index=True)
    print(df.columns)


    # TODO: add historic playing time as a factor ?? 
    feature_columns = [
        "attack_defence_ratio",
        "ict_index_normalized_avg",
        "influence_normalized_avg",
        "creativity_normalized_avg",
        "threat_normalized_avg",
        "expected_goals_avg"
    ]

    # Some target columns to model against
    target_columns = [
        # More fluid values
        #"expected_assists",
        #"expected_goals",
        "expected_goals_per_minute",
        #"expected_goal_involvements",
        #"expected_goals_conceded",
        #"total_points",
       # "bps",

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

    X = df[feature_columns].values
    y = df[target_columns[0]].values 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Training samples {len(X_train)}")
    print(f"Test samples {len(X_test)}")

    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Define the objective function for Optuna
    def objective(trial):
        params = {
            'max_depth': trial.suggest_int('max_depth', 4, 15),
            'learning_rate': trial.suggest_float('learning_rate', 1e-3, 1.0, log=True),
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
            'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
            'gamma': trial.suggest_float('gamma', 1e-8, 1.0, log=True)
        }
        
        # K-fold cross-validation
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = []
        
        for train_idx, val_idx in kf.split(X_train_scaled):
            X_train_fold, X_val_fold = X_train_scaled[train_idx], X_train_scaled[val_idx]
            y_train_fold, y_val_fold = y_train[train_idx], y_train[val_idx]
            
            model: xgb.XGBRegressor = xgb.XGBRegressor(
                **params,
                early_stopping_rounds=50,
                eval_metric="rmse",
                random_state=42
                )
            model.fit(X_train_fold, y_train_fold,
                      eval_set=[(X_val_fold, y_val_fold)],
                      verbose=False)
            
            y_pred = model.predict(X_val_fold)
            mse = mean_squared_error(y_val_fold, y_pred)
            cv_scores.append(mse)
        
        return np.mean(cv_scores)
    # Run Optuna optimization
    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=25)
    
    # Get the best parameters
    best_params = study.best_params
    print("Best parameters:", best_params)
    
    # Train the final model with the best parameters
    best_model = xgb.XGBRegressor(
        **best_params, 
        early_stopping_rounds=50,
        eval_metric="rmse",
        random_state=42)

    best_model.fit(X_train_scaled, y_train,
                   eval_set=[(X_test_scaled, y_test)],
                   verbose=False)
    
    y_pred = best_model.predict(X_test_scaled)


    # Calculate performance metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared Score: {r2}")

    # Apply model to df
    # Extract and scale features from the DataFrame
    X_full_scaled = scaler.transform(df[feature_columns].values)

    # Generate predictions
    df['predicted_expected_goals_per_minute'] = best_model.predict(X_full_scaled)
    df['predicted_expected_goals'] = df['predicted_expected_goals_per_minute']* df['minutes']


    df_p = df[df["name"] == "Erling Haaland"]
    print_df(df_p[[
        #*feature_columns, 
        "predicted_expected_goals",
        "expected_goals",
        "goals_scored",
        "minutes"
        ]])

    plot_and_save(
        df_p,
        actual_col='expected_goals',
        predicted_col='predicted_expected_goals',
        output_dir='plots',
        filename='xgboost_expected_goals_plot.png'
    )


    plot_crossplot(
        y_true=y_test,
        y_pred=y_pred,
        mse=mse,
        r2=r2,
        output_dir='plots',
        filename='xgboost_crossplot.png'
    )

    # Example usage of the plot_feature_importance function
    plot_feature_importance(
        model=best_model,
        feature_columns=feature_columns,
        output_dir='plots',
        filename='xgboost_feature_importance.png'
    )    

train_model("2023-24")


