"""Player object"""
import pandas as pd

class Player:
    """Snapshot of a player at a given gameweek 
    Baseclass storing the player's name, position, cost and points"""
    def __init__(self, p_data, gamweek: int, is_captain: bool = False, is_vice_captain: bool = False):
        """Player is set from a pandas dataset series with data.
        Args:
            p_data (pandas dataset series)
            gamweek (int): gameweek 
            is_captain (bool): is the player the captain 
            is_vice_captain (bool): is the player the vice captain
        """
        self.p_data = p_data
        self.total_points   = p_data.total_points
        self.__set_constant_metadata()
        self.is_captain = is_captain
        self.is_vice_captain = is_vice_captain
        self.gameweek = gamweek

    def __set_constant_metadata(self):
        """private function to set the constant metadata of the player"""
        self.id             = self.p_data.id
        self.player_name    = self.p_data.name
        self.position       = self.p_data.position
        self.cost           = self.p_data.cost
        self.team           = self.p_data.team

    def update_gameweek_data(self, df: pd.Series, gameweek:int):
        """Update the player's gameweek data"""
        self.p_data = df
        self.gameweek = gameweek
        self.__set_constant_metadata()

    def player_points(self):
        """Return the player's points for the gameweek"""
        return self.p_data.total_points

    def player_summary(self):
        print(f"Name: \t{self.player_name}")
        print(f"Pos: \t{self.position}")
        print(f"Cost: \t{self.cost}")
        print(f"Points: {self.total_points}")