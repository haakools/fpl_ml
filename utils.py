"""
File utilies
"""

import pandas as pd



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

