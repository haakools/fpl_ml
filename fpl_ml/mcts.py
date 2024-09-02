"""
Monte Carlo Tree Search algorithm

SELECTION
Start from root node R until a leaf node is reached
Leaf node is any node that has a potential child
from which no simulation has been initiated

EXPANSION
unless the leaf node ends the game (impossible in this context)
create one (or more) child nodes and choose node C from one of them.
Child nodes are any valid moves from the game position in leaf node L

SIMULATION
Complete one random (or biased by ML model) playout from node C.

BACKPROPAGATION
The points will be added back to the root divided by around 2400 (typical fantasy score?)
"""
from typing import List
import math
from itertools import count
import random

from fpl_ml.lib.team import Team
from fpl_ml.gameweek_database import GameweekDatabase


# Scalar values --> needed for numerical stablity if future use???
MAX_POINTS_FOR_SEASON = 3000 # guessed maximum points in a season. seems large enough
MAX_POINTS_FOR_A_ROUND = MAX_POINTS_FOR_SEASON/38 #~78

class MCTSNode:
    def __init__(self, state: Team, parent=None):
        self.state: Team = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

        self.tried_action_hashes = parent.tried_action_hashes
        self.untried_actions = self.get_untried_actions()

        self.hash = None #self.generate_team()

    def generate_team(self, retry=count(), max_retry:int = 5) -> str:
        """Make a gameweek change. Returns hash of team to pass to parent node"""
        # TODO: Need to compare with hash of other parts. 
        # Randomness and weighting will help for now
        if retry == max_retry: 
            print("Generated the same hash 5 times in a row")
            return 

        self.state.set_team()
        team_hash = self.state.get_team_hash()
        if team_hash in self.tried_action_hashes:
            counter = next(retry)
            return self.get_untried_actions(retry=counter)
        return team_hash
   
    def select_child(self):
        """UCB1 Formula"""
        return max(self.children, key=lambda c: c.value / c.visits + 
                   math.sqrt(2 * math.log(self.visits) / c.visits))

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.apply_action(action)
        child = MCTSNode(next_state, parent=self)
        self.children.append(child)

        return child

    def update(self, reward):
        self.visits += 1
        self.value += reward

class MCTS:
    def __init__(self, 
                 root_team: Team, 
                 database: GameweekDatabase,
                 max_depth = 10, 
                 iterations=1000, exploration_weight=1.4):
        self.root: MCTSNode = MCTSNode(root_team, [])
        self.database: GameweekDatabase = database
        self.iterations = iterations
        self.exploration_weight = exploration_weight
        self.max_depth = max_depth

    def search(self):
        for _ in range(self.iterations):
            node = self.select_node(self.root)
            reward = self.simulate(node.state)
            self.backpropagate(node, reward)

        return self.best_action(self.root)

    def select_node(self, node: MCTSNode):
        while node.untried_actions == [] and node.children != []:
            node = node.select_child()
        if node.untried_actions != []:
            return node.expand()
        return node

    def simulate(self, node, depth=0):
        while depth < self.max_depth:
            # !!
            action = random.choice(node.state.get_legal_actions())
            state = node.state.apply_action(action)
            depth += 1
        return state.get_reward()

    def backpropagate(self, node, reward):
        while node is not None:
            node.update(reward)
            node = node.parent

    def best_action(self, node):
        return max(node.children, key=lambda c: c.visits).state.last_action
