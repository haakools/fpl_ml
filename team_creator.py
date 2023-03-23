"""This is a class that branches out the different states of the team

After a new gameweek is loaded and points are tallied up, branch out N different scenarios
for the next gameweek, i.e. states or cells.

The differences should be:
    - transfers
    - captain changes
    - vice captain changes
    - bench changes
    - no changes 
"""
import team

class TeamState:
    """This class contains the logic to find the next state of the team.
    It will keep track of which states have already been applied and apply new ones. 
    It will also be capped.
    """

    def __init__(self, team: team.Team, gameweek: int, N_leaf_nodes: int = 100):
        """Initialize the team state

        Args:
            team (Team): The team object
            gameweek (int): The gameweek
            N_leaf_nodes (int, optional): The number of branches to make. Defaults to 100.
        """
        self.team = team
        self.gameweek = gameweek
        self.N_leaf_nodes = N_leaf_nodes
        self.branches = []
        self.branches.append(self.get_team_state())

    def get_team_state(self):
        """Return the team state
        This should return what the team state is, i.e.
            - What is the starting team
            - Who is the captain
            - Who is the vice captain
            - What is the bench
        And get that as an unique object that is easily comparable.
        """
        pass
    
    def create_leaf_nodes(self):
        """Create N leaf nodes"""
        pass 


