"""Module defining a player"""
from dataclasses import dataclass
from typing import Any
import sys
import json

import pandas as pd



@dataclass
class Player:
    def __init__(self, id:int, series: pd.Series, gameweek: int) -> None:
        self.id = id
        self.gameweek = gameweek
        self.series = series
        self.team: str = self.series["team"].iloc[self.gameweek-1]
        self.team_code: str = self.series["team_code"].iloc[self.gameweek-1]
        self.name: str = self.series["name"].iloc[self.gameweek-1]
        self.position: str = self.series["position"].iloc[self.gameweek-1]

    def change_gameweek(self, gameweek: int) -> None:
        self.gameweek = gameweek

    def __repr__(self) -> str:
        return f"""
            player ID {self.id}
            player name {self.name}
            team {self.team}
            team_code {self.team_code}
            position {self.position}
        """

    def to_json(self):
        return self.series.to_dict(orient="records")
    
    def print_json(self):
        return print(json.dumps(self.to_json(), indent=4))
