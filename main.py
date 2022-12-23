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
    simulation_fn = simulation_greedy
    error = {'greedy': 0, 'tabucol': 0, 'nmcs_dsatur': 0, 'nmcs_degree': 0, 'nrpa': 0, 'nrpa_dsatur': 0}
    n_samples = 30
    
    nmcs_dsatur = NMCS(simulation_fn, get_possible_moves_by_Dsatur)
    nmcs_degree = NMCS(simulation_fn, get_possible_moves_by_node_degree)
    for i in range(n_samples):
        graph = dataset[i]
        print(len(graph.G.nodes()))
        root = SearchNode(graph, None)
        greedy = Greedy(nx.to_numpy_matrix(graph.G))
        n_colors_greedy = greedy.execute()

        nrpa = NRPA(graph, get_possible_moves_by_node_degree, upper_bound_colors=n_colors_greedy + 2)
        nrpa_dstaur = NRPA(graph, get_possible_moves_by_Dsatur, upper_bound_colors=n_colors_greedy + 2)

        nrpa_dsatur_score, solution_nrpa_dsatur = nrpa.run(level=4)


        start = time()

        nrpa_score, solution_nrpa = nrpa.run(level=4)


        print('NRPA time', time() - start)
        
        start = time()

        nmcs_dsatur_score, solution_dsatur = nmcs_dsatur.run(root, level=5)

        print('NMCS dsatur time:', time() - start)

        start = time()

        nmcs_degree_score, solution_degree = nmcs_degree.run(root, level=5)

        print('NMCS degree time:', time() - start)

        if not solution_dsatur.check_coloring():
            print('Something went wrong no solution dsatur')

        if not solution_degree.check_coloring():
            print('Something went wrong no solution degree')

        if not solution_nrpa.check_coloring():
            print('Something went wrong no solution NRPA')

        if not solution_dsatur.check_coloring() or not solution_degree.check_coloring() or not solution_nrpa.check_coloring():
            continue

        assert len(solution_dsatur.get_uncolored_nodes()) == 0
        assert len(solution_degree.get_uncolored_nodes()) == 0
        assert len(solution_nrpa.get_uncolored_nodes()) == 0
        print('True chormatic number: ', graph.true_n_colors)
        print('NMCS dsatur: ', -nmcs_dsatur_score)
        print('NMCS degree: ', -nmcs_degree_score)
        print('NRPA dsatur: ', -nrpa_dsatur_score)
        print('NRPA: ', -nrpa_score)
        print('Greedy:', n_colors_greedy)

        for tabucol_n_colors in range(graph.true_n_colors, n_colors_greedy + 1):
            print('N colors tabucol', tabucol_n_colors)
            solution = tabucol(nx.to_numpy_matrix(graph.G), tabucol_n_colors, reps=100, max_iterations=1000)
            if solution is not None:
                print('Tabucol: ', len(set(solution.values())))
                break
            else:
                print('Tabucol could not find solution')
        error['nmcs_dsatur'] += -nmcs_dsatur_score - graph.true_n_colors
        error['nmcs_degree'] += -nmcs_degree_score - graph.true_n_colors
        error['nrpa'] += -nrpa_score - graph.true_n_colors
        error['nrpa_dsatur'] += -nrpa_dsatur_score - graph.true_n_colors
        error['greedy'] += n_colors_greedy - graph.true_n_colors
        error['tabucol'] += tabucol_n_colors - graph.true_n_colors

    print('Mean error: ')
    print('NMCS dsatur: ', error['nmcs_dsatur'] / n_samples)
    print('NMCS degree: ', error['nmcs_degree'] / n_samples)
    print('NRPA dsatur: ', error['nrpa_dsatur'] / n_samples)
    print('NRPA: ', error['nrpa'] / n_samples)
    print('Greedy: ', error['greedy'] / n_samples)
    print('Tabucol: ', error['tabucol'] / n_samples)
