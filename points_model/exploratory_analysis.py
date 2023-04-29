"""Stack the gameweeks together."""

import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import matplotlib.pyplot as plt
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# TODO: GET THIS FROM THE API
LATEST_GAMEWEEK = 33

# wanted features 
features = ['minutes', 'expected_goals', 'expected_assists',
             'expected_goals_conceded', 'expected_goal_involvements',
             'own_goals', 'clean_sheets', 'goals_conceded',
             'yellow_cards', 'red_cards', 'influence', 'creativity',
             'threat', 'ict_index']

target = ['total_points']


def create_dataset(dataset: np.ndarray, look_back: int = 1):
    """Convert an array of values into a dataset matrix."""
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i+look_back), :]
        dataX.append(a)
        dataY.append(dataset[i+look_back, :])
    return np.array(dataX), np.array(dataY)


def get_position_data(position: str) -> list[int]:
    """Given a position (GK, DEF, MID, FWD), gets all the available player ids for that position
    Doctest:
    >>> gk_ids = get_position_data("GK")
    >>> def_ids = get_position_data("DEF")
    >>> mid_ids = get_position_data("MID")
    >>> fwd_ids = get_position_data("FWD")
    >>> assert not any([id in def_ids for id in mid_ids])
    >>> assert not any([id in fwd_ids for id in mid_ids])
    >>> assert not any([id in fwd_ids for id in def_ids])
    """
    player_ids = []

    # this looks horrible. get this number from the api instead
    gameweek_csv_list = os.listdir("gameweek")
    last_gameweek = sorted([int(file.split(".")[0].split("_")[1]) for file in gameweek_csv_list])[-1]

    df = pd.read_csv(f"gameweek/gameweek_{last_gameweek}.csv")
    df = df.loc[df.position == position]
    player_ids.extend(df.id.values.tolist())
    return player_ids

def create_position_dataset(position:str, look_back: int = 1):
    """Get the player data of every player"""
    if position not in ["GK", "DEF", "MID", "FWD"]:
        raise ValueError("Invalid position. Must be one of GK, DEF, MID, FWD")

    position_ids = get_position_data(position)

    total_X_train = []
    total_X_test = []
    total_y_train = []
    total_y_test = []

    train_size = int(LATEST_GAMEWEEK * 0.8)


    for id in position_ids:
        # loading player data
        player_df = pd.read_csv(f"player_history/{id}.csv", index_col=0)

        if len(player_df) < LATEST_GAMEWEEK-1:
            # dropping player if they werent here from the start
            # TODO: Fix this 
            continue

        # Getting the important features
        features_df = player_df[features]
        dataset = features_df.values

        # TODO: create a model that converts expected features_df to target_df
        #target_df = player_df[target]

        # Splitting
        test_size = len(dataset) - train_size
        train, test = dataset[:train_size], dataset[train_size:]        

        # Creating time series for that player. Using look_back = 1 for now
        X_train, y_train  = create_dataset(train.astype(np.float32), look_back = look_back)
        X_test, y_test = create_dataset(test.astype(np.float32), look_back = look_back)

        # Reshaping 
        #X_train = np.expand_dims(X_train, axis = 1)
        #X_test =  np.expand_dims(X_test, axis = 1)

        # adding to the total dataset
        total_X_train.append(X_train)
        total_X_test.append(X_test)
        total_y_train.append(y_train)
        total_y_test.append(y_test)
   
    return np.array(total_X_train), np.array(total_X_test), \
        np.array(total_y_train), np.array(total_y_test)


def main():
    """"Main function for running multivariate time series forecasting.

    Notes:
        Want to predict the total points of a player given their features. Starting with
        feature t-1 to predict feature t. TODO is to predict the total number of points
        given the features of the player AND the opponent team strength. opponent team strength
        could be calculated by an ELO model or something that characterizes the strength of the 
        enemies defence and attack.
    
    Multivariate time series forecasting
    TODO: find out how to factor in the opponent team and their strength rating
    """
    # Create midfielder model    
    X_train, X_test, y_train, y_test = create_position_dataset("MID")
    X_train = np.squeeze(X_train)
    X_test = np.squeeze(X_test)
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

    # Scaling. Must reshape the the data and shape it back again. 
    # X_train.shape # 102, 24, 1, 14 (players, gameweeks,  features)
    # TODO: Unittest/pytest that this reshaping is correct
    scaler = StandardScaler()
    X_train_normed = scaler.fit_transform(X_train.reshape(-1, X_train.shape[-1]))
    X_train_normed = X_train_normed.reshape(*X_train.shape)
    scaler_dims = 1, X_train.shape[1]
    X_test_normed = scaler.transform(X_test.reshape(-1, X_test.shape[-1]))
    X_test_normed = X_test_normed.reshape(*X_test.shape)

    X_train = torch.from_numpy(X_train_normed)
    y_train = torch.from_numpy(y_train)
    X_test = torch.from_numpy(X_test_normed)
    y_test = torch.from_numpy(y_test)

    class ShallowLSTM(nn.Module):
        def __init__(self):
            super().__init__()
            self.lstm = nn.LSTM(
                input_size = len(features),
                hidden_size = 100,
                num_layers = 1,
                batch_first = True
                )
            self.linear = nn.Linear(100, len(features))

        def forward(self, x):
            x, _ = self.lstm(x)
            x = self.linear(x)
            return x

    def train_model():
        model = ShallowLSTM()
        optimizer = optim.Adam(model.parameters())
        loss_fn = nn.MSELoss()
        assert type(X_train) == torch.Tensor
        assert type(y_train) == torch.Tensor
        loader = data.DataLoader(
            data.TensorDataset(X_train, y_train), shuffle=True, batch_size=1)

        n_epochs = 100
        for epoch in range(n_epochs):
            model.train()
            for X_batch, y_batch in loader:
                y_pred = model(X_batch)
                loss = loss_fn(y_pred, y_batch)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            # Validation
            if epoch % 10 != 0:
                continue
            model.eval()
            with torch.no_grad():
                y_pred = model(X_train)
                train_rmse = np.sqrt(loss_fn(y_pred, y_train))
                y_pred = model(X_test)
                test_rmse = np.sqrt(loss_fn(y_pred, y_test))
            print("Epoch %d: train RMSE %.4f, test RMSE %.4f" % (epoch, train_rmse, test_rmse))
        return model

    trained_model = train_model()

    # predict the model on the test set
    x_test_sample = X_test[-1]
    y_test_sample = y_test[-1]

    y_pred_sample = trained_model(x_test_sample.unsqueeze(0))

    # reshaping and rescaling
    ground_truth = np.squeeze(y_test_sample.detach().numpy()).reshape(1, len(features))
    prediction = np.squeeze(y_pred_sample.detach().numpy()).reshape(1, len(features))

    # rescaling back
    ground_truth = scaler.inverse_transform(ground_truth)
    prediction = scaler.inverse_transform(prediction)

    for i, feature in enumerate(features):
        print(f"{feature}: {ground_truth[:, i]} {prediction[:, i]}")

    # plotting 
    plt.bar(np.arange(len(features)), np.squeeze(ground_truth), label = "target", alpha=0.5)
    plt.bar(np.arange(len(features)), np.squeeze(prediction), label = "prediction", alpha=0.5)
    plt.xticks(np.arange(len(features)), features, rotation=90)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
