# 
A tool that creates an optimal strategy for Premier League Fantasy. This is *not* meant to be a bot that can play fantasy for you, but rather a statistical tool to help assess the optimal, expected transfers and captains to be done to optimize points.

Scenarioes this tool could be helpful is when multiple factors are at play.
Given -4 points for each transfer exceeding those that are available, with the maximum of 3 stored (new rules 24/25 season), it might become very complex trying to plan for planning the next 5 rounds. 
If you then add in double gameweeks in the later part of the season, optimizing chips like wildcard, triple captain, freehit (assuming the mystery chip), it might become highly extrenaeous to have a qualitative argument for team selection.

## Implementation roadmap

 - Create a naive Monte Carlo Tree Search, using a simplistic xP model
 - Implement opposition difficulty, with more finely weighted with defense and offense difficuly than the FDR (Fixture Difficulty Rating)
 - Possibility to see top N most rewarding paths for player to choose
 - Factor in probablities of team succeeding to later stages in FA-cup (making double gameweeks more probable).
 - Investigate how to implement more risk into the analysis, i.e. selecting player node-paths that have a higher variance.
 - Create a react website to host a page where you can analyze your own team



## Setup

Setup submodules

```
git submodule init
git submodule update --remote --recursive
```

Setup virtual env

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```





