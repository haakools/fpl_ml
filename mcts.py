"""
Monte Carlo Tree Search algorithm

https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
"""
import math


# Find out more about how the data will look like before diving into the code




class MCTS:
    """Monte carlo tree search algorithm"""

    def __init__(self, exploration_weight=1.4):
        self.Q = {}  # total reward of each node 
        self.N = {}  # number of visits of each node
        self.P = {}  # prior probability of each node
        self.children = {}  # children of each node
        self.exploration_weight = exploration_weight


    def choose(self, node):
        """Choose the best action to take at the current state
        I.e. choose a move before a gameweek starts """
        if node.is_terminal():
            # why runtimeerror?
            raise RuntimeError("choose called on terminal node")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            """Calculate the UCB score for a node"""
            if self.N[n] == 0
                return float("-inf") # avoid unseen moves
            # average reward of the node. (reward of the node / number of visits of the node) 
            return self.Q[n] / self.N[n] 

        return max(self.children[node], key=score) # return the node with the highest score

    def do_rollout(self, node):
        """Do a rollout from the current node until the end of the game
        Returns the reward of all the nodes visited during the rollout"""
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        # NOTE: this should return the reward of all the nodes leading up to the leaf!
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

    def _select(self, node):
        """Find an unexplored descendent of `node`"""
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)

    def _expand(self, node):
        """Updatre the `children` dict with the children of `node`"""
        if node in self.children:
            return # already expanded
        self.children[node] = node.find_children()





















