"""Module defining a player"""
from dataclasses import dataclass



@dataclass
class Player:
    def __init__(self, first_name: str, last_name: str, id:int) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.id = id



