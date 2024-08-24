
import requests
import json
from typing import List
from dataclasses import dataclass

@dataclass
class PersonalTeamInfo:
    team_id: str
    summary: dict
    gameweek: int
    gameweek_data: dict
    available_transfers: int

    def budget(self) -> int:
        """budget in pounds * 10"""
        return next(
            e.get("bank")
            for e in self.summary.get("current", [])
            if e.get("event") == self.gameweek
        )
    
    def chips_used(self) -> str:
        return self.summary.get("chips")


    def player_ids(self) -> List[str]:
        return [pick.get("element") for pick in self.gameweek_data.get("picks")]
    
    def __repr__(self) -> str:
        return f"""
            TEAM_ID {self.team_id}
            Chips used {self.chips_used()}
            Starting at gameweek {self.gameweek}
            Current Budget: {self.budget()}
            Available transfers: {self.available_transfers}
        """


class FplApiHandler:

    def __init__(self) -> None:
        self.entry_endpoint =  f"https://fantasy.premierleague.com/api/entry/"

    def calculate_available_transfers(self, all_gameweek_data: str) -> int:
        # check if the API has a counter for this instead of calculating myself
        # todo write unit test for this function
        available_transfers = 1
        for gameweek in reversed(all_gameweek_data):
            entry_history = gameweek.get("event_history", {})
            if int(entry_history.get("event_transfers_cost", "0"))>0:
                return 1 
            event_transfers = int(entry_history.get("event_transfers", "0"))
            if event_transfers == 0:
                available_transfers = min(available_transfers+1, 3)
            else:
                available_transfers = 1 + max(0, available_transfers - event_transfers)
        return available_transfers

    def get_personal_team_info(self, team_id):
        summary = self.get_entry_data(team_id)  
        current_gameweek = len(summary.get("current"))
        gameweek_data = self.get_gameweek_data(team_id, current_gameweek)

        all_gameweek_data = self.get_entry_gameweeks_data(team_id, current_gameweek)
        available_transfers = self.calculate_available_transfers(all_gameweek_data)

        return PersonalTeamInfo(team_id, summary, current_gameweek, 
                                gameweek_data, available_transfers)


    def get_request(self, endpoint, timeout=15):
        try:
            response: requests.Response = requests.get(endpoint, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            print(f"Connection error occurred while trying to reach {endpoint}")
        except requests.exceptions.Timeout:
            print(f"Request timed out while trying to reach {endpoint}")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            print(f"Status code: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected error occurred: {e}")

        except json.JSONDecodeError:
            print("Failed to parse the response as JSON")

    def get_personal_entry_data(self, entry_id: str) -> dict:
        data = self.get_request(
            self.entry_endpoint + f"{entry_id}"
        )
        if data:
            return data

    def get_gameweek_data(self, entry_id: str, gameweek: str) -> dict:
        data = self.get_request(
            self.entry_endpoint + f"{entry_id}/event/{gameweek}/picks/"
        )
        if data:
            return data

    def get_entry_gameweeks_data(self, entry_id: str, num_gws: int, start_gw: int=1) -> List[dict]:
        gw_data = []
        for gw in range(start_gw, num_gws+1):
            data = self.get_gameweek_data(entry_id, gw)
            if data: gw_data += [data]
        return gw_data
    
    def get_entry_data(self, entry_id: str) -> dict:
        data = self.get_request(
            self.entry_endpoint + f"{entry_id}/history/"
        )
        if data: 
            return data


