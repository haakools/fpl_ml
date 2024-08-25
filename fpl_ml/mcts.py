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
import math
import random

from fpl_ml.lib.team import Team
from gameweek_database import GameweekDatabase


def hash_objects(object_list: list):
    # TODO: test that this would ensure the same hash for different orders
    return hash(tuple(object_list))

# Scaler values
MAX_POINTS_FOR_SEASON = 3000
MAX_POINTS_FOR_A_ROUND = MAX_POINTS_FOR_SEASON/38 #~78

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        self.untried_actions = self.get_untried_actions()

    def get_untried_actions(self):
        # Return a list of untried actions from the current state
        pass

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
        self.root: MCTSNode = MCTSNode(root_team)
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

    def select_node(self, node):
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
