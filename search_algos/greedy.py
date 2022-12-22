import random
import networkx as nx
import numpy as np
import os
from tree.graph import Graph
import scipy


class Greedy:
    def __init__(self, adj_matr, is_stochastic=False):
        self.adj_matr = adj_matr
        self.n = int(adj_matr.shape[0])
        self.colors = np.zeros(self.n, dtype=np.int32) - 1
        self.is_stochastic = is_stochastic

    def execute(self):
        if self.is_stochastic:
            first_vertex = random.randrange(self.n)
        else:
            first_vertex = 0
        self.color_vertex(first_vertex)
        return np.max(self.colors) + 1

    def color_vertex(self, vertex):
        is_possible = False
        vertex_color = 0
        while not is_possible:
            for i in range(self.n):
                if self.adj_matr[vertex, i] == 1 and vertex_color == self.colors[i]:
                    vertex_color += 1
                    break
                if i == self.n - 1:
                    is_possible = True
        self.colors[vertex] = vertex_color

        for i in range(self.n):
            if self.adj_matr[vertex, i] == 1 and self.colors[i] == -1:
                self.color_vertex(i)

class Greedy_V2:
    '''Greedy starting from some already colored graph'''
    def __init__(self, G: Graph, stochastic=False, iters=10) -> None:
        self.G = G.copy()
        self.stochastic = stochastic
        self.adj_matr = nx.to_numpy_matrix(G.G)

    def run(self):
        nx.set_node_attributes(self.G.G, {node : 0 for node in self.G.G.nodes}, "importance")
        
        while len(self.G.get_uncolored_nodes()) > 0:
            starting_node = list(self.G.get_uncolored_nodes())[0]
            self.color_node(starting_node)
        return max(self.G.used_colors()) + 1

    def color_node(self, node):
        possible_colors = self.G.get_possible_colorings_by_node(node)
        self.G.set_node_color(node, min(possible_colors))

        neighboors = list(filter(lambda x: nx.get_node_attributes(self.G.G, "color").get(x) is None, self.G.G.neighbors(node)))
        # sort w.r.t. importance
        attrs = nx.get_node_attributes(self.G.G, 'importance')
        if len(neighboors) == 0:
            return

        if self.stochastic:
            sorted_neighboors = [(node, attrs[node]) for node in neighboors]
            nodes_order = [item[0] for item in sorted_neighboors]
            probabilities = scipy.special.softmax([item[1] for item in sorted_neighboors])
            sorted_neighboors = np.random.choice(nodes_order, size=len(nodes_order), replace=False, p=probabilities)
            for neighboor in sorted_neighboors:
                self.color_node(neighboor)
        else:
            attrs = nx.get_node_attributes(self.G.G, 'importance')
            sorted_neighboors = [(node, attrs[node]) for node in neighboors]
            sorted_neighboors.sort(key=lambda x: x[1])
            sorted_neighboors = [item[0] for item in sorted_neighboors]
            for neighboor in sorted_neighboors:
                self.color_node(neighboor)

class WeightenedStochasticGreedy:
    def __init__(self,G: Graph, get_moves_fn, action_weights=None, upper_bound_colors=None) -> None:
        actions = {}
        self.G = G
        self.get_moves_fn = get_moves_fn
        if action_weights is None:
            nodes_list = list(G.G.nodes())
            if upper_bound_colors is None:
                raise RuntimeError('Either action weights should be provided either upper bound for colors')
            self.ub = upper_bound_colors
            colors = upper_bound_colors
            action_weights = {node: {color: 0 for color in  range(colors)} for node in nodes_list}
        self.action_weights = action_weights
        self.ub = max(list(self.action_weights[0].keys()))

    def run(self):
        G = self.G.copy()
        uncolored_nodes = G.get_uncolored_nodes()
        while len(uncolored_nodes) > 0:
            moves = self.get_moves_fn(G)
            max_color = max([item[1] for item in moves])
            if max_color > self.ub:
                return -self.ub - 1, None
            probabilities = scipy.special.softmax([self.action_weights[item[0]][item[1]] for item in moves])
            chose_move_ind = np.random.choice(len(moves), size=1, replace=False, p=probabilities)[0]
            # print(chose_move_ind)
            G.set_node_color(moves[chose_move_ind][0], moves[chose_move_ind][1])

            uncolored_nodes = G.get_uncolored_nodes()
        return -len(G.used_colors()), G


if __name__ == '__main__':
    from ColorDataset import ColorDataset
    root = 'dataset_40_60'
    dataset = ColorDataset(root)
    sample = dataset[3]
    greedy = Greedy_V2(sample, stochastic=True)
    colors_greedy = greedy.run()
    print('True chromatic number: ', sample.true_n_colors)
    print('Greedy V2: ', colors_greedy)
