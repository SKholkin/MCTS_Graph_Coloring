from tree.graph import Graph
import numpy as np
from search_algos.greedy import Greedy_V2

class SearchNode:
    def __init__(self, state: Graph, parent) -> None:
        # state new G
        self.value = 0
        self.state = state
        self.is_explored = None
        self.n_played = None
        self.avg_value = None
        self.children = []
    
    def explore(self):
        # get new G
        # actions is set of pairs (node, color)
        actions = self.state.get_possible_moves()
        for act in actions:
            new_G = self.state.copy()
            node_act = act[0]
            color_act = act[1]
            new_G.set_node_color(node_act, color_act)
            self.children.append(SearchNode(new_G, self))

        return self.children

    def best_child(self):
        if not self.is_explored:
            return self
        best_ind = np.argmax([child.value for child in self.children])
        return self.children[best_ind]   


class SearchTree:
    def __init__(self, root: SearchNode) -> None:
        self.root = root

    def select(self):
        selected_node = self.root
        depth = 1
        seq = []
        while True:
            seq.append(selected_node)
            best_child = selected_node.best_child()
            if best_child == selected_node:
                break
            selected_node = best_child
            depth += 1
        return selected_node, depth, seq

def random_policy(G, possible_actions):
    return [1 / len(possible_actions)  for i in range(len(possible_actions))]
    
def simulation(G: Graph):
    G = G.copy()
    uncolored_nodes = G.get_uncolored_nodes()
    while len(uncolored_nodes) > 0:
        possible_actions = G.get_possible_moves()
        probabilities = random_policy(G, possible_actions)
        ind_choice = np.random.choice(len(possible_actions), 1, p=probabilities)[0]
        G.set_node_color(possible_actions[ind_choice][0], possible_actions[ind_choice][1])
        uncolored_nodes = G.get_uncolored_nodes()
    reward = -len(G.used_colors())
    return reward, G

def simulation_greedy(G):
    greedy = Greedy_V2(G, stochastic=True)
    colors = greedy.run()
    assert len(greedy.G.get_uncolored_nodes()) == 0

    return -colors, greedy.G
    