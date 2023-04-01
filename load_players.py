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
    return players

def update_player_list(players: List[player.Player], gameweek: int) -> List[player.Player]:
    """Updates the player list to the gameweek given"""
    df = gameweek_dict[gameweek]
    for p in players:
        p.update_gameweek_data(df.loc[df.id == p.id].iloc[0], gameweek)
    return players 

if __name__ == "__main__":
    # Selecting a player
    gameweek = 1
    p_selected = load_all_gameweeks_players(gameweek)[5]

    print(f"Gameweek: {p_selected.gameweek}")
    print(f"Selected player: {p_selected.player_name}")
    print(f"Selected player data: {p_selected.p_data}")
    p_selected.player_summary()

    # Updating the gameweek
    gameweek = 20
    p_selected = update_player_list([p_selected], gameweek)[0]

    print(f"Gameweek: {p_selected.gameweek}")
    print(f"Selected player: {p_selected.player_name}")
    print(f"Selected player data: {p_selected.p_data}")
    p_selected.player_summary()

