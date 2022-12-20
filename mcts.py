from graph import Graph
import numpy as np
import networkx as nx

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
        print('possible_actions', possible_actions)
        ind_choice = np.random.choice(len(possible_actions), 1, p=probabilities)[0]
        G.set_node_color(possible_actions[ind_choice][0], possible_actions[ind_choice][1])
        uncolored_nodes = G.get_uncolored_nodes()
    reward = -len(G.used_colors())
    return reward, G
    

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
            print('Depth', depth)
            print(type(tree.root.state))
            print(tree.root.state.get_uncolored_nodes())
            print('Selected node (Graph) uncolored nodes ', selected_node.state.get_uncolored_nodes())

            # exploration
            to_explore_nodes = selected_node.explore()

            # simulation
            for child in to_explore_nodes:
                print('Selected node (Graph) uncolored nodes ', child.state.get_uncolored_nodes())
                reward_list = []
                for n_sim in range(number_of_simulations):
                   reward, result_G = simulation(child.state)
                   reward_list.append(reward)
                   print('Colored graph', nx.get_node_attributes(result_G.G, "color"), nx.to_numpy_matrix(result_G.G))
                   input()
                reward = np.mean(reward_list)

            # backpropagation
            # child.backpropagate()
        return best_seq

if __name__ == '__main__':
    G = Graph(nx.to_numpy_matrix(nx.star_graph(5)), 5)
    mcts = MCTS(G)
    mcts.run()
