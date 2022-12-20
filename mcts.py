from graph import Graph
import numpy as np

class SearchNode:
    def __init__(self, state: Graph, parent) -> None:
        # state new G
        self.value = 0
        self.state = state
        self.G = Graph()
        self.is_explored = None
        self.n_played = None
        self.avg_value = None
        self.children = []
    
    def explore(self):
        # get new G
        # actions is set of pairs (node, color)
        actions = self.G.possible_moves()
        for act in actions:
            new_G = self.G.copy()
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
        choice = np.random.choice(possible_actions, 1, p=probabilities)
        G.set_node_color(choice[0], choice[1])
        uncolored_nodes = G.get_uncolored_nodes()
    reward = -G.used_colors()
    return reward
    

class MCTS:
    def __init__(self, G) -> None:
        self.G = G

    def run(self):
        n_episodes = 1
        number_of_simulations = 10
        tree = SearchTree(SearchNode(self.G.copy(), None))
        best_seq = []
        for i in range(n_episodes):
            # selection
            selected_node, depth, seq = tree.select()

            # exploration
            to_explore_nodes = selected_node.explore()

            # simulation
            for child in to_explore_nodes:
                reward_list = []
                for n_sim in range(number_of_simulations):
                   reward = simulation(child.state)
                   reward_list.append(reward)
                reward = np.mean(reward_list)
            
            # backpropagation
            # child.backpropagate()
        return best_seq
