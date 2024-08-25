
import requests
import pandas as pd
import os


MAX_GAMEWEEKS = 38
SEASON = "2024-25"

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
        # Player and team mapping
        self.player_maps = {
            str(elements_df["id"].iloc[i]): 
            {
                "first_name": elements_df['first_name'].iloc[i],
                "second_name": elements_df['second_name'].iloc[i],
                "team": elements_df['team'].iloc[i],
                "team_code": elements_df['team_code'].iloc[i],
            }

            for i in range(len(elements_df))
        }

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
            player_map = self.player_maps[str(player["id"])]
            full_player_name = player_map.get("first_name") +\
                " " + player_map.get("second_name")
            player_stats[full_player_name] = {**player["stats"]}
            player_stats[full_player_name].update({"id": player["id"]})
            player_stats[full_player_name].update(player_map, )
        gameweek_stats[str(gameweek_number)] = player_stats

        # Saving to disk
        df = pd.DataFrame(player_stats).T
        directory =f"data/season_{SEASON}"
        os.makedirs(directory, exist_ok=True)
        df = df.reset_index()  # This will make the index a column
        df = df.rename(columns={'index': 'player_name'})  # Rename the new column to 'player_name'
        df.to_csv(directory+ f"/gameweek_{gameweek_number}.csv", index=False)
        return True

if __name__ == "__main__":
    client = FantasyPremierLeagueAPI()
    client.download_data()