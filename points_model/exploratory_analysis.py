"""
Stack the gameweeks together.

"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from load_players import gameweek_dict


def stack_gameweeks(gameweek_dict: dict) -> pd.DataFrame:
    """Stacks the gameweeks together

    Args:
    ----
        gameweek_dict (dict): dictionary of gameweeks

    Returns:
    ----
        pd.DataFrame: stacked gameweeks
    """
    df = pd.concat(gameweek_dict.values(), ignore_index=False)
    df["cost"] = df["cost"].astype(int)
    return df


def main():
    df = stack_gameweeks(gameweek_dict)

    # Print all the columns
    print(df.columns)

    # Filter out the players with minutes played less than 60
    df = df[df["minutes"] >= 60]

    # Plot the histogram of points
    df["total_points"].groupby(df["position"]).hist(bins=15, alpha=0.5, legend=True)
    plt.show()

    # crossplot of points vs cost
    df["total_points"] = df["total_points"].astype(int)
    df.groupby("position").plot.scatter(x="cost", y="total_points")
    df.plot.scatter(x="cost", y="total_points")
    plt.show()


    #print(df.head(len(df)))

if __name__ == "__main__":
    main()