from tree.graph import Graph
import numpy as np
from search_algos.greedy import WeightenedStochasticGreedy
from ColorDataset import ColorDataset
import scipy
import networkx as nx


class NRPA:
    def __init__(self, G: Graph, get_moves_fn, upper_bound_colors, iterations=5, alpha=0.1, turn_off_adapt=False) -> None:
        # pair (node number, color)
        self.turn_off_adapt = turn_off_adapt
        self.G = G
        self.alpha = alpha
        self.get_moves_fn = get_moves_fn
        self.iterations = iterations
        self.ub = upper_bound_colors
        self.policy = {node: {color: 0 for color in range(self.ub)} for node in list(self.G.G.nodes())}

    def adapt_policy(self, solution):
        node_colors = nx.get_node_attributes(solution.G, "color")
        for node, color in node_colors.items():
            self.policy[node][color] += self.alpha
            # for color in range(self.upper_bound_colors):
            prob = scipy.special.softmax([self.policy[node][c] for c in range(self.ub)])
            for c in range(len(prob)):
                self.policy[node][c] -= self.alpha * prob[c]

    def run(self, level=5):
        if level == 0:
            greedy = WeightenedStochasticGreedy(self.G, self.get_moves_fn, action_weights=self.policy)
            reward, solution = greedy.run()
            return reward, solution
        best_score = -np.inf
        best_solution = None
        for i in range(self.iterations):
            reward, solution = self.run(level=level - 1)
            if reward >= best_score and solution is not None:
                best_score = reward
                best_solution = solution
            if not self.turn_off_adapt and best_solution is not None:
                self.adapt_policy(best_solution)
        return best_score, best_solution

if __name__ == '__main__':
    from tree.graph import get_possible_moves_by_node_degree
    root = 'dataset_40_60' 
    dataset = ColorDataset(root)
    graph = dataset[0]
    from search_algos.greedy import Greedy, Greedy_V2
    import networkx as nx
    greedy = Greedy_V2(graph)
    ub = greedy.run()
    print('Upper Bound ', ub)
    nrpa = NRPA(graph, get_possible_moves_by_node_degree, upper_bound_colors=ub)
    reward, best_solution = nrpa.run(level=3)
    print(f'NRPA : ', -reward)

