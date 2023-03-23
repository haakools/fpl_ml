import enum
from typing import List


from utils import load_csv
import player

class Position(enum.Enum):
    """double check what the values are inside the dataset"""
    GK = 1
    DEF = 2
    MID = 3
    FWD = 4

class Team:
    """Class for handling the team and its players"""
    def __init__(
            self,
            gameweek: int,
            goalkeepers: List[player.Player],
            defenders: List[player.Player],
            midfielders: List[player.Player],
            forwards: List[player.Player],
            budget: int,
            ):
        """Initialise the team with the players and budget for a given gameweek""" 
        self.gameweek = gameweek
        self.goalkeepers = goalkeepers
        self.defenders = defenders
        self.midfielders = midfielders
        self.forwards = forwards

        self.budget = None
        self.transfers_available = None # :int, maximum 2. Always 1

        self.captain = None # player.Player
        self.vice_captain = None # player.Player
        self.starting = None # list of 11 players. composition of players needs to be correct!
        self.bench = None # list of 4 players, ORDER MATTERS



    def set_starting(self, starting):
        """Set the starting team"""
        # Always needs to be a goalkeeper


        self.verify_starting(starting)
        self.starting = starting    

    def verify_position(self, position: Position, players: List[player.Player]) -> bool:
        """Verify the position is valid"""
        for player in players:
            if player.position != position:
                raise ValueError(f"Player {player.player_name} is not a {position}")


    def verify_starting(self, starting) -> bool:
        """Verify the starting team is valid"""
        if len(starting) != 11:
            return False

        if len(starting) != len(set(starting)):
            return False

        if self.captain not in starting:
            return False

        if self.budget < 0:
            return False

        return True

    def set_captain(self, captain): 
        """Only setting the captain to a player in the starting team"""
        self.captain = captain if captain in self.starting else None

    def change_player(self, sell_player: List[player.Player], buy_player: List[player.Player]):
        """Change a player in the starting team"""
        # The positions of each of the player in sell_player needs to be the same as the buy_player
        # Check if the player in the sell_player and buy_player are the same

        self.starting.remove(sell_player)
        self.starting.append(buy_player)


    def play_out_gameweek(self, gameweek: int):
        """
        Iterative function to play out the gameweek.
        1. Loads the next gameweek data
        2. Adds points to each player in the starting team. 
            If minutes played is 0, then look for substitutes 
            from the bench in the correct order.  
            If minutes played on the captain is 0, then 
            double the score for the vice captain (there are no third captain)

        After this, branch out N different scenarios for the next gameweek, i.e. states. 
        This should be 
            - transfers
            - captain changes
            - vice captain changes
            - bench changes
            - no changes 
        """
        total_points = 0

        if self.captain.minutes != 0:
            total_points += 2 * self.captain.player_points()
        else:
            total_points += self.vice_captain.player_points() 

        # This requires the self.bench list to be correctly ordered as wished
        subs = [player for player in self.bench if player.minutes != 0]




        for player in self.starting:
               total_points += player.player_points()
        return total_points


if __name__ == "__main__":
    # Load gameweek 1 and all its players
    gameweek = 1
    file = f"gameweek/gameweek_{gameweek}.csv"
    df = load_csv(file)
    players = [df.iloc[:,i] for i in range(len(df))]

    p1 = player.Player(players[0], gameweek)
    p1.player_summary()

