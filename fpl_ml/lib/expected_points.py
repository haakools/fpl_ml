"""
First implementation of a fairly NAIVE model.

Calculating expected points for a given fixture is a difficult task.

This model will only take in-season data and do a simplified heuristic 
to get an estimate.
The bonus point system is available to see, but an historical average will suffice.


Factors to consider weighting
1. Minutes > 45 --> FOR ALL
2. Historical bonus points average (expected)

GOALKEEPER
1. Expected goals conceded 
2. Team Defense Quality / Opposition Offense Quality

DEFENDER
1. Expected goals conceded as low as possible.
2. Team Defense Quality / Opposition Offense Quality
3. Expected goals*goalpoints + Expected assists*assistpoints

MIDFIELD
2. Team Defense Quality / Opposition Offense Quality
3. Expected goals*goalpoints + Expected assists*assistpoints


"""

from fpl_ml.lib.player import Player

class ExpectedPointsModel:
    def __init__(self) -> None:
        pass


    def get_points(self, player: Player):
        player_position = player.position
        match player_position:
            case "GK":
                return

            case "DEF":
                return
            
            case "MID":
                return

            case "FWD":
                return
            case _:
                raise ValueError(f"ERROR: COULD NOT FIND POSITION FOR PLAYER {player}")
            
