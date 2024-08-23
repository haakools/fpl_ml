

import os
from typing import Any

import pandas as pd

CURRENT_YEAR = 2024

class GameweeekDatabase:

    def __init__(self) -> None:
        self.year = CURRENT_YEAR
        self.csv_dir = f"data/season_{self.year}"

    def load_database(self):

        csv_paths = os.listdir(self.csv_dir) 
        print(f"Found {len(csv_paths)} csv paths for year {self.year}")

        df_list = []
        for csv_path in csv_paths:
            df = pd.read_csv(csv_path, index_col=None)
            df_list.append(df)

        self.df = pd.concat(df_list, axis=0, ignore_index=True)



    

