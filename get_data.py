
import requests
import pandas as pd
import os


MAX_GAMEWEEKS = 38
YEAR = 2024

class FantasyPremierLeagueAPI:
    def __init__(self):
        pass

    def get_player_map(self):
        url = "https://fantasy.premierleague.com/api/bootstrap-static/"
        r = requests.get(url)
        content = r.json()

        elements_df = pd.DataFrame(content["elements"])
        elements_types_df = pd.DataFrame(content["element_types"])
        teams_df = pd.DataFrame(content["teams"])

        # PLAYER ID MAPPING
        player_map = {}
        for i in range(len(elements_df)):
            index = elements_df['id'].iloc[i]
            first_name = elements_df['first_name'].iloc[i]
            second_name = elements_df['second_name'].iloc[i]
            player_map[str(index)] = first_name + " " + second_name
        self.player_map = player_map

    def download_data(self):
        if not hasattr(self, "player_map" ):
            self.get_player_map()

        for i in range(1, MAX_GAMEWEEKS):
            if not self.download_gameweek(i):
                break

    def download_gameweek(self, gameweek_number:str) -> bool:
        gameweek_stats = {}
        player_stats = {}
        reply = requests.get(f"https://fantasy.premierleague.com/api/event/{gameweek_number}/live/")
        players = reply.json()["elements"]

        print(f"Found {len(players)} for gameweek {gameweek_number}")
        if len(players) == 0:
            return False

        for player in players:
            player_name = self.player_map[str(player["id"])]
            player_stats[player_name] = player["stats"]
        gameweek_stats[str(gameweek_number)] = player_stats

        # Saving to disk
        df = pd.DataFrame(player_stats)
        directory =f"data/season_{YEAR}"
        os.makedirs(directory, exist_ok=True)
        df.to_csv(directory+ f"/gameweek_{gameweek_number}.csv")
        return True

if __name__ == "__main__":
    client = FantasyPremierLeagueAPI()
    client.download_data()