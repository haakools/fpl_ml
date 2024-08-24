import os
from typing import Any

import pandas as pd
from lib.player import Player


CURRENT_SEASON = "2024-25"

class GameweeekDatabase:
    def __init__(self) -> None:
        self.season = CURRENT_SEASON
        #self.csv_dir = os.path.join("..", f"data/season_{self.season}")
        self.csv_dir = f"data/season_{self.season}"

    def load_database(self):
        csv_paths = os.listdir(self.csv_dir) 
        print(f"Found {len(csv_paths)} csv paths for {self.season}")

        df_list = []
        for csv_path in csv_paths:
            df = pd.read_csv(os.path.join(self.csv_dir, csv_path), index_col=None)
            df_list.append(df)

        self.df = pd.concat(df_list, axis=0, ignore_index=True)


    def create_player(self, player_id: str):
        print(self.df)

        return Player