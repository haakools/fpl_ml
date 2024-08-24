
import requests
import json
from typing import List

class FplApiHandler:


    def __init__(self) -> None:
        self.entry_endpoint =  f"https://fantasy.premierleague.com/api/entry/"


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

