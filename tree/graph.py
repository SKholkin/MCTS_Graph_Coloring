import networkx as nx
import numpy as np
from copy import deepcopy
import random

class Graph:
    def __init__(self, adj_matr, true_n_colors) -> None:
        self.true_n_colors = true_n_colors
        self.G = nx.from_numpy_matrix(np.array(adj_matr))
        self.adj_matr = np.array(adj_matr)

    def set_node_color(self, node, color):
        nx.set_node_attributes(self.G, {node: color}, name='color')

    def copy(self):
        return deepcopy(self)

    def order_nodes(self, nodes: set):
        nodes = list(nodes)
        random.shuffle(nodes)
        return nodes

    def used_colors(self):
        attrs = nx.get_node_attributes(self.G, "color").values()
        ret_val = set(attrs)
        return ret_val

    def get_uncolored_nodes(self):
        colored_vertices = set(nx.get_node_attributes(self.G, "color").keys())
        return set(list(range(self.G.number_of_nodes()))) - colored_vertices
    
    @staticmethod
    def get_available_colors(busted_colors):
        # for the case of zero colors
        if len(busted_colors) == 0:
            return set([0])
        if max(busted_colors) + 1 == len(busted_colors):
            return set([max(busted_colors) + 1])
        set_1 = set(range(max(busted_colors) + 1))
        set_2 = busted_colors
        return set_1 - set_2
    
    def get_possible_colorings_by_node(self, n_node):
        # all the neighboors nodes and available colors
        neighbors = self.G.neighbors(n_node)
        busted_colors = set()
        for neigh_node in neighbors:
            # get available colors
            color = nx.get_node_attributes(self.G, "color").get(neigh_node)
            if color is not None:
                busted_colors.add(color) 

        available_colors = self.get_available_colors(busted_colors)
        return available_colors

    def check_coloring(self):
        coloring = nx.get_node_attributes(self.G, "color")
        for colored_node in coloring.keys():
           for vertex_2 in coloring.keys():
                if self.adj_matr[colored_node, vertex_2] == 1:
                    if coloring[colored_node] == coloring[vertex_2]:
                        return False
        return True


def get_possible_moves_random(self):
    # choose uncolored node by some order (random at the moment 4.2 https://hal.archives-ouvertes.fr/hal-03118170/file/MonteCarloGraphColoring.pdf)
    
    # 1. Take all the uncolored nodes that do connect with already colored nodes
    # 2. Chose one of them randomly
    # 3. Return all the available colorings of this node
    colored_vertices = set(nx.get_node_attributes(self.G, "color").keys())

    vertices_to_color = self.get_uncolored_nodes()
    # seach for a connected one
    if len(colored_vertices) > 0:
        connected_vertices_to_color = []
        for vertex in vertices_to_color:
            for vertex_2 in colored_vertices:
                if self.adj_matr[vertex, vertex_2] == 1:
                    connected_vertices_to_color.append(vertex)
                    break
    else:
        connected_vertices_to_color = vertices_to_color

    connected_vertices_to_color = vertices_to_color

    # choosing random node of all availables
    chosen_ind = np.random.choice(len(connected_vertices_to_color))

    chosen_node = self.order_nodes(connected_vertices_to_color)[chosen_ind]
    # all possible colors for this node wil be moves
    busted_colors = set()
    for neigh_node in self.G.neighbors(chosen_node):
        color = nx.get_node_attributes(self.G, "color").get(neigh_node)
        if color is not None:
            busted_colors.add(color) 
    available_colors = self.get_available_colors(busted_colors)
    return [(chosen_node, color) for color in available_colors]

def get_possible_moves_by_Dsatur(self):
    uncolored_nodes = self.get_uncolored_nodes()
    n_colors_by_node = {node: 0 for node in uncolored_nodes}
    for node in uncolored_nodes:
        colors = self.get_possible_colorings_by_node(node)
        n_colors_by_node[node] = len(colors)

    chosen_node = list({k: v for k, v in sorted(n_colors_by_node.items(), key=lambda item: item[1])}.keys())[0]

    colors = self.get_possible_colorings_by_node(chosen_node)
    return [(chosen_node, color) for color in colors]


def get_possible_moves_by_node_degree(self):
    uncolored_nodes = self.get_uncolored_nodes()
    degrees = {node: self.G.degree(node) for node in uncolored_nodes}

    chosen_node = list({k: v for k, v in sorted(degrees.items(), key=lambda item: item[1], reverse=True)}.keys())[0]

    colors = self.get_possible_colorings_by_node(chosen_node)
    return [(chosen_node, color) for color in colors]

def get_possible_moves_v1(self):
    # Not efficient

    # 1. Take all the not colored nodes
    # 2. Chose first of them
    # 3. Return all the possible coloring for her
    vertices_to_color = self.get_uncolored_nodes()
    chosen_node = self.order_nodes(vertices_to_color)[0]
    # all possible colors for this node wil be moves
    busted_colors = set()
    for neigh_node in self.G.neighbors(chosen_node):
        color = nx.get_node_attributes(self.G, "color").get(neigh_node)
        if color is not None:
            busted_colors.add(color)

    available_colors = self.get_available_colors(busted_colors)
    return [(chosen_node, color) for color in available_colors]


if __name__ == '__main__':
    busted_colors = set([0, 1, 2, 4])
    print(Graph.get_available_colors(busted_colors))
