
# Create a tool that creates an optimal strategy for Premier League Fantasy

The goal:
 - Given your team, it should calculate what the optimal strategy for the next N rounds are.
 - Host this on a webpage with some javascript framework


How to achieve this:
 - Get the python wrapper for fantasy premier league to download some data
 - Create first a $t=0$ strategy based on the most popular team for fantasy after the first gameweek this season (2022/23)
 - https://www.analyticsvidhya.com/blog/2022/09/uninformed-search-strategy-for-state-space-search-solving/ 


Maybe not MCTS ??? 
Each depth would be a gameweek, where every node would be a change in 
transfers, captain, benchplayers.

 - Make a monte carlo tree search where each depth is a gameweek.





