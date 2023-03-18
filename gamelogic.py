import enum
from utils import load_csv

class Position(enum.Enum):
    """double check what the values are inside the dataset"""
    GK = 1
    DEF = 2
    MID = 3
    FWD = 4


class Player:
    """Baseclass storing the player's name, position, cost and points"""
    def __init__(self):
        self.name = None
        self.position = None
        self.cost = None
        self.points = None
        self.team = None

    #def 


    def __repr__(self):
        """Return a string representation of the player"""
        return f"{self.name} ({self.position.name})"



class Team:
    """Class for handling the team and its players"""
    def __init__(self):
        self.starting = None # list of 11 players
        self.goalkeepers = None
        self.defenders = None
        self.midfielders = None
        self.forwards = None
        self.budget = None
        self.captain = None

    def set_starting(self, starting):
        self.starting = starting    

    def verify_starting(self):
        """Verify that the starting team is valid"""
        if len(self.starting) != 11:
            raise ValueError("Starting team must have 11 players")
        if self.captain not in self.starting:
            raise ValueError("Captain must be in starting team")
        if sum(p.cost for p in self.starting) > self.budget:
            raise ValueError("Starting team exceeds budget")





if __name__ == "__main__":

    file = "gameweek/gameweek_1.csv"
    df = load_csv(file)
    print(df.head())
    exit()
    player = Player()
    player.name = df["name"][0]
    player.position = Position(df["position"][0])
    player.cost = df["cost"][0]
    player.points = df["points"][0]
    player.team = df["team"][0]

    player.__repr__()





