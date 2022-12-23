import torch
from torch.utils.data import Dataset
import os
from tree.graph import Graph
import networkx as nx
import numpy as np

def adj_matr_to_adj_list(adj_matr):
    adj_list = [[] for i in range(len(adj_matr))]
    adj_matr = adj_matr.copy()
    for i in range(len(adj_matr)):
        for j in range(len(adj_matr)):
            if adj_matr[i][j] == 1:
                adj_list[i].append(j)
                adj_list[j].append(i)
                adj_matr[i][j] = 0
                adj_matr[j][i] = 0
    return adj_list

def adj_list_to_adj_matr(adj_list):
    adj_matr = [([0 for j in range(len(adj_list))]) for i in adj_list]
    for i, vertex_info in enumerate(adj_list):
        for j in vertex_info:
            adj_matr[i][j] = 1
    return adj_matr

def _transform_to_instance(adj_matr, n_colors, is_solvable, v_size=30, c_size=11):
    # get final matrice instances to put them into GNN
    # Mvv [V,V] adj matr 0 or 1
    # Mvc [V,C] vertex-to-color 1
    # V vertex embeddings from normal
    # C color embeddings (not for each vertex) from uniform
    adj_matr = torch.tensor([[adj_matr[i][j] if (len(adj_matr) > max(j, i)) else 0 for j in range(v_size)]
                             for i in range(v_size)], dtype=torch.float32)
    return adj_matr, n_colors, is_solvable

def _transform_to_instance(adj_matr, n_colors, is_solvable, v_size=30, c_size=11):
    if not is_solvable:
        raise ValueError('Not solvable graph in dataset')
    graph = nx.from_numpy_matrix(np.array(adj_matr))
    is_connected = nx.is_connected(graph)
    if not is_connected:
        print('Not connected')
    return Graph(adj_matr, n_colors)

class ColorDataset(Dataset):
    def __init__(self, root, is_train=True):
        self.root = root
        self.info = torch.load((os.path.join(root,  f'{"train" if is_train else "test"}_info.pt')))
        self.max_size = self.info['nmax']
        self.max_n_colors = self.info['max_n_colors']
        mode = 'train' if is_train else 'test'
        cut_on = 100
        basic_data = [torch.load(os.path.join(root, mode, item)) for item in
                               list(os.listdir(os.path.join(root, mode)))[:cut_on]]
        self.data = []
        for graph_info in basic_data:
            adj_matr = np.array(adj_list_to_adj_matr(graph_info['adj_list']))
            graph = nx.from_numpy_matrix(np.array(adj_matr))
            is_connected = nx.is_connected(graph)
            if graph_info['is_solvable'] and is_connected:
                self.data.append((graph_info['adj_list'], graph_info['n_colors'], graph_info['is_solvable']))
                

    def __getitem__(self, idx):
        # get instance through transformation
        adj_matr = adj_list_to_adj_matr(self.data[idx][0])
        n_color = self.data[idx][1]
        is_solvable = self.data[idx][2]
        return _transform_to_instance(adj_matr, n_color, is_solvable, v_size=self.max_size, c_size=self.max_n_colors)

    def __len__(self):
        return len(self.data)

if __name__ == '__main__':
    root = 'dataset_40_60'
    dataset = ColorDataset(root)
    print(len(dataset))
    instance = dataset[0]
