"""
Monte Carlo Tree Search algorithm

https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
"""
import math

from lib.team import Team

def hash_objects(object_list: list):
    # TODO: test that this would ensure the same hash for different orders
    return hash(tuple(object_list))


# Start from root node R until a leaf node is reached
# Leaf node is any node that has a potential child
# from which no simulation has been initiated

# expansion
# unless the leaf node ends the game (impossible in this context)
# create one (or more) child nodes and choose node C from one of them.
# Child nodes are any valid moves from the game position in leaf node L

# Simulation
# Complete one random (or biased by ML model) playout from node C.

# Backpropagation
# The points will be added back to the root divided by around 2400 (typical fantasy score?)


MAX_POINTS_FOR_SEASON = 3000
MAX_POINTS_FOR_A_ROUND = MAX_POINTS_FOR_SEASON/38 #~78


class MCTSNode:
    def __init__(self, state: Team, parent=None):
        self.state = state # Team (?)
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

class MCTS:
    def __init__(self, exploration_weight=1.4):
        self.exploration_weight = exploration_weight

    def choose(self, node):
        if not node.children:
            return self.expand(node)
        return max(node.children, key=self.uct_score)

    def expand(self, node):
        tried_children = {c.state for c in node.children}

        # find_random_child would need to have some bias and legal moves

        new_state = node.state.find_random_child()
        while new_state in tried_children:
            new_state = node.state.find_random_child()
        child = MCTSNode(new_state, parent=node)
        node.children.append(child)
        return child

    def simulate(self, node):
        inplace_state = node.state
        while not inplace_state.is_terminal():
            inplace_state = inplace_state.move(inplace_state.find_random_move())
        return inplace_state.reward()

    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent

    def uct_score(self, child):
        if child.visits == 0:
            return float('inf')
        return (child.value / child.visits) + self.exploration_weight * math.sqrt(
            math.log(child.parent.visits) / child.visits
        )

    def search(self, initial_state, n_iterations=1000):
        root = MCTSNode(initial_state)

        for _ in range(n_iterations):
            node = root
            while node.children:
                node = self.choose(node)
            
            if node.visits == 0:
                reward = self.simulate(node)
                self.backpropagate(node, reward)
            else:
                child = self.expand(node)
                reward = self.simulate(child)
                self.backpropagate(child, reward)

        return max(root.children, key=lambda c: c.visits).state
