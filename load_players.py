"""Functions for loading a list of players"""
import pandas as pd
import os
from typing import List

import player
import utils

# Loaded into memory at the start of the program
gameweek_dict = {
    gameweek_counter: utils.load_csv(f"gameweek/gameweek_{gameweek_counter}.csv") 
    for gameweek_counter in range(1, len(os.listdir("gameweek")) + 1)
}

def load_all_gameweeks_players(gameweek: int) -> List[player.Player]:
    """Load the all players from the csv file for a given gameweek

    Args:
    ----
        gameweek (int): gameweek

    Returns:
    ----
        List[player.Player]: list of players
    """
    df = gameweek_dict[gameweek]
    players = []
    for _, row in df.iterrows():
        players.append(player.Player(row, gameweek))
    gk_players = [p for p in players if p.position == "GK"]    
    def_players = [p for p in players if p.position == "DEF"]
    mid_players = [p for p in players if p.position == "MID"]
    fwd_players = [p for p in players if p.position == "FWD"]
    return gk_players, def_players, mid_players, fwd_players 

def update_player_list(players: List[player.Player], gameweek: int) -> List[player.Player]:
    """Updates the player list to the gameweek given"""
    df = gameweek_dict[gameweek]
    for p in players:
        p.update_gameweek_data(df.loc[df.id == p.id].iloc[0], gameweek)
    return players 

if __name__ == "__main__":
    # Selecting a player
    gameweek = 1
    GK, DEF, MID, FWD = load_all_gameweeks_players(gameweek)[5]

    print(f"Gameweek: {GK.gameweek}")
    print(f"Selected player: {GK.player_name}")
    print(f"Selected player data: {GK.p_data}")
    GK.player_summary()

    # Updating the gameweek
    gameweek = 20
    GK = update_player_list(GK, gameweek)[0]

    print(f"Gameweek: {GK.gameweek}")
    print(f"Selected player: {GK.player_name}")
    print(f"Selected player data: {GK.p_data}")
    GK.player_summary()
