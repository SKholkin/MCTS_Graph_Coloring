from graph import Graph
from mcts import simulation
from tree_search import SearchNode, SearchTree
import networkx as nx

class NMCS:
    def __init__(self) -> None:
        self.tree = None

    def nmcs_search(self, G):
        pass

    def run(self, node: SearchNode, level):
        # run NMCS starting from G

        if level == 0:
            score, seq = simulation(node.state)
            return score, seq

        uncolored_nodes = node.state.get_uncolored_nodes()
        
        current_graph = node.state
        best_score = -10000
        
        while len(uncolored_nodes) > 0:
            possible_actions = node.state.get_possible_moves()
            prev_graph = current_graph
            for action in possible_actions:
                new_G = current_graph.copy()
                new_G.set_node_color(action[0], action[1])
                new_node = SearchNode(new_G, self)
                new_score, new_solution = self.run(new_node, level - 1)
                if new_score > best_score:
                    best_score = new_score
                    current_graph = new_G
                    best_solution = new_solution

            if current_graph == prev_graph:
                return best_score, best_solution
            uncolored_nodes = current_graph.get_uncolored_nodes()
            #print('uncolored_nodes', uncolored_nodes)
        return best_score, current_graph


class NMCS_V2:
    def __init__(self) -> None:
        pass

    def nmcs(self, node: SearchNode, level):
        
        if level == 0:
            score, seq = simulation(node.state)
            return score, seq

        uncolored_nodes = node.state.get_uncolored_nodes()
        
        current_graph = node.state
        best_score = -10000
        
        while len(uncolored_nodes) > 0:
            possible_actions = node.state.get_possible_moves()
            prev_graph = current_graph
            for action in possible_actions:
                new_G = current_graph.copy()
                new_G.set_node_color(action[0], action[1])
                new_node = SearchNode(new_G, self)
                new_score, new_solution = self.nmcs(new_node, level - 1)
                if new_score >= best_score:
                    best_score = new_score
                    current_graph = new_G
                    best_solution = new_solution

            if current_graph == prev_graph:
                return best_score, best_solution
            uncolored_nodes = current_graph.get_uncolored_nodes()
            #print('uncolored_nodes', uncolored_nodes)
        return best_score, current_graph

    def run(self, node: SearchNode, level):
        pass


if __name__ == '__main__':
    nmcs = NMCS()
    G = Graph(nx.to_numpy_matrix(nx.star_graph(10)), 5)
    root = SearchNode(G, None)
    score, solution = nmcs.run(root, level=3)
    print(solution.used_colors())
    print(set(nx.get_node_attributes(solution.G, "color").values()))

    print(score, nx.get_node_attributes(solution.G, "color"))
