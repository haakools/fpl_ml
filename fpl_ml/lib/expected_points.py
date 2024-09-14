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
import os
import json

from fpl_ml.lib.player import Player


class ExpectedPointsModel:
    def __init__(self, player_fixtures,  save_folder: str = "expectedpoints") -> None:
        self.save_folder = save_folder
        self.player_fixtures = player_fixtures

    def get_points(self, player: Player):
        player_position = player.position
        print(player_position)
        if player_position == "GK":
            # 1. Expected goals conceded 
            # 2. Team Defense Quality / Opposition Offense Quality
            return
        elif player_position == "DEF":

            # 1. Expected goals conceded as low as possible.
            # 2. Team Defense Quality / Opposition Offense Quality
            # 3. Expected goals*goalpoints + Expected assists*assistpoints
            return
        elif player_position == "MID":

            return
        elif player_position == "FWD":

            return
        else:
            raise ValueError(f"ERROR: COULD NOT FIND POSITION FOR PLAYER {player}")
        


        #match player_position:
        #    case "GK":
        #        return

        #    case "DEF":
        #        return
        #    
        #    case "MID":
        #        return

        #    case "FWD":
        #        return
        #    case _:
        #        raise ValueError(f"ERROR: COULD NOT FIND POSITION FOR PLAYER {player}")
            







