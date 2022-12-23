# MCTS_Graph_Coloring
Repo for applying Monte Carlo Tree Search technics for Graph Coloring Problem

## Dataset 

You can generate dataset by running
`python dataset_generator.py --samples N_samples --nmin min_n_of_vertices --nmax max_n_of_vertices --root path_to_dataset`

Or download dataset containing around 32000 graphs with 40 to 60 vertices it from https://drive.google.com/file/d/1tGd9bDSfJf6tt8gUZxYXZU5iBGL4ISj9/view?usp=sharing 

## Run experiments

`python main.py --dataset <path_to_generated_dataset>`
