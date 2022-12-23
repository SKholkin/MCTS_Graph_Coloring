from ColorDataset import ColorDataset
from search_algos.nmcs import NMCS
from tree.tree_search import SearchNode
import networkx as nx
from search_algos.greedy import Greedy
from tabucol import tabucol
from tree.tree_search import simulation_greedy, simulation
from tree.graph import get_possible_moves_random, get_possible_moves_by_Dsatur, get_possible_moves_by_node_degree
from search_algos.nrpa import NRPA
from time import time

if __name__ == '__main__':
    
    root = 'dataset_30_45'
    dataset = ColorDataset(root)
    print(len(dataset))
    simulation_fn = simulation_greedy
    error = {'greedy': 0, 'tabucol': 0, 'nmcs_dsatur': 0, 'nmcs_degree': 0, 'nrpa': 0, 'nrpa_dsatur': 0}
    n_samples = 30
    nmcs_degree = NMCS(simulation_fn, get_possible_moves_by_node_degree)
    levels = [2, 3, 5, 7, 8]
    error_dict = {item: 0 for item in levels}
    time_dict = {item: 0 for item in levels}
    
    for i in range(n_samples):
        graph = dataset[i]
        print(len(graph.G.nodes()))
        greedy = Greedy(nx.to_numpy_matrix(graph.G))
        n_colors_greedy = greedy.execute()
        for param in levels:
            root = SearchNode(graph, None)
            start_time = time()
            nmcs_score, solution = nmcs_degree.run(root, level=param)
            error_dict[param] += (-nmcs_score - graph.true_n_colors)
            time_dict[param] += time() - start_time
            print(param, '  ', (-nmcs_score), 'vs ', graph.true_n_colors , time() - start_time)
        
    print('Mean error: ', {key: value / len(error_dict.values()) for key, value in error_dict.items()})
    print('Mean time: ', {key: value / len(time_dict.values()) for key, value in time_dict.items()})
