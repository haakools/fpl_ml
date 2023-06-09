"""Player object"""
import pandas as pd

# TODO: Initialize this player class with the player_history csvs instead of gameweek csvs


class Player:
    """Snapshot of a player at a given gameweek 
    Baseclass storing the player's name, position, cost/price and points"""
    def __init__(
            self,
            history_df: pd.DataFrame,
            metadata_df: pd.DataFrame,
            is_captain: bool = False,
            is_vice_captain: bool = False
            ):
        """Player is set from a pandas dataset series with data.
        Args:
            stats_df (pd.DataFrame) : dataframe of player_history
            metadata_df (pd.DataFrame) : dataframe of player metadata (name, position, team, etc.)
            gamweek (int): gameweek 
            is_captain (bool): is the player the captain 
            is_vice_captain (bool): is the player the vice captain
        """
        self.history_df = history_df
        self.__set_history_data()

        self.metadata_df = metadata_df
        self.__set_constant_metadata()
        self.is_captain = is_captain
        self.is_vice_captain = is_vice_captain

    def __set_history_data(self):
        """Parsing the history_df dataframe and inserting into lists"""





    def __set_constant_metadata(self):
        """private function to set the constant metadata of the player"""


        self.id             = self.p_data.id
        self.player_name    = self.p_data.name
        self.position       = self.p_data.position
        self.price           = self.p_data.cost
        self.team           = self.p_data.team

        # TODO: add more metadata
        self.threat        = self.p_data.threat

    def update_gameweek_data(self, df: pd.Series, gameweek:int):
        """Update the player's gameweek data"""
        self.p_data     = df
        self.gameweek   = gameweek
        self.__set_constant_metadata()

    def get_round_points(self):
        """Return the player's points for the gameweek"""
        return self.p_data.round_points

    def player_summary(self):
        print(f"Name: \t{self.player_name}")
        print(f"Team: \t{self.team}")
        print(f"Pos: \t{self.position}")
        print(f"Cost: \t{self.price}")
        print(f"Points: {self.round_points}")


if __name__ == "__main__":
    history_df = pd.read_csv("player_history/1.csv")
    metadata_df = pd.read_csv("metadata.csv")


    player = Player(history_df, metadata_df) 
    player.player_summary()


