

import json


from fpl_ml.gameweek_database  import GameweekDatabase
from fpl_ml.lib.expected_points import ExpectedPointsModel


season = "2023-24"
database = GameweekDatabase(season)
database.load_database()





team_fixtures = database.team_fixtures[season]
team_ratings = database.team_ratings[season]
team_code_map = database.team_code_map[season]




#print(json.dumps(team_ratings, indent=4))
#print(team_code_map) # keys are 1-20, values are interseason IDs

gameweek = 2 # should only return one match played, the rest non-statted
player_fixtures = database.generate_player_fixture_list(gameweek)


print(json.dumps(team_fixtures[1], indent=4))
print(len(team_fixtures))
points_model = ExpectedPointsModel(player_fixtures)

points_model
#expected_points_per_match = points_model.expected_points()


