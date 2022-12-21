from ColorDataset import ColorDataset
from search_algos.nmcs import NMCS
from tree.tree_search import SearchNode
import networkx as nx
from search_algos.greedy import Greedy
from tabucol import tabucol

if __name__ == '__main__':
    root = 'dataset_40_60'
    dataset = ColorDataset(root)
    for i in range(30):
        graph = dataset[i]
        nmcs = NMCS()
        root = SearchNode(graph, None)
        greedy = Greedy(nx.to_numpy_matrix(graph.G))
        n_colors_greedy = greedy.execute()
        score, solution = nmcs.run(root, level=5)
        print('True chormatic number: ', graph.true_n_colors)
        print('NMCS: ', -score)
        print('Greedy:', n_colors_greedy)
        for n_colors in range(graph.true_n_colors, n_colors_greedy + 1):
            print('N colors tabucol', n_colors)
            solution = tabucol(nx.to_numpy_matrix(graph.G), n_colors)
            if solution is not None:
                print('Tabucol: ', len(set(solution.values())))
                break
            else:
                print('Tabucol could not find solution')
