"""
File utilies
"""

import pandas as pd
import json


def load_csv(file_path):
    """
    Load csv file
    """
    return pd.read_csv(file_path, index_col=0)

def save_csv(df, file_path):
    """
    Save csv file
    """
    df.to_csv(file_path)

def save_to_json(dict: dict) -> None:
    """
    Save dictionary to json file
    """
    with open('data.json', 'w') as f:
        json.dump(dict, f, indent=4)

def load_from_json(file_path) -> dict:
    """
    Load dictionary from json file
    """
    with open(file_path, 'r') as f:
        return json.load(f)