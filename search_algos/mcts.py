from graph import Graph
import numpy as np
import networkx as nx
from tree_search import SearchNode, SearchTree, simulation

    
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
