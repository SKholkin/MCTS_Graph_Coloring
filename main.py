from ColorDataset import ColorDataset
from search_algos.nmcs import NMCS
from tree.tree_search import SearchNode
import networkx as nx
from search_algos.greedy import Greedy
from tabucol import tabucol
from tree.tree_search import simulation_greedy, simulation
from tree.graph import get_possible_moves, get_possible_moves_by_Dsatur, get_possible_moves_by_node_degree



if __name__ == '__main__':
    root = 'dataset_40_60'
    dataset = ColorDataset(root)
    simulation_fn = simulation_greedy
    get_moves_fn = get_possible_moves
    error = {'nmcs': 0, 'greedy': 0, 'tabucol': 0}
    n_samples = 30
    for i in range(n_samples):
        graph = dataset[i]
        nmcs = NMCS(simulation_fn, get_moves_fn)
        root = SearchNode(graph, None)
        greedy = Greedy(nx.to_numpy_matrix(graph.G))
        n_colors_greedy = greedy.execute()
        nmcs_score, solution = nmcs.run(root, level=5)
        print(f'Number of non colored nodes: ', len(solution.get_uncolored_nodes()))
        assert len(solution.get_uncolored_nodes()) == 0
        print('True chormatic number: ', graph.true_n_colors)
        print('NMCS: ', -nmcs_score)
        print('Greedy:', n_colors_greedy)

        for tabucol_n_colors in range(graph.true_n_colors, n_colors_greedy + 1):
            print('N colors tabucol', tabucol_n_colors)
            solution = tabucol(nx.to_numpy_matrix(graph.G), tabucol_n_colors)
            if solution is not None:
                print('Tabucol: ', len(set(solution.values())))
                break
            else:
                print('Tabucol could not find solution')
        error['nmcs'] += -nmcs_score - graph.true_n_colors
        error['greedy'] += n_colors_greedy - graph.true_n_colors
        error['tabucol'] += tabucol_n_colors - graph.true_n_colors
    print('Mean error: ')
    print('NMCS: ', error['nmcs'] / n_samples)
    print('Greedy: ', error['greedy'] / n_samples)
    print('Tabucol: ', error['tabucol'] / n_samples)
