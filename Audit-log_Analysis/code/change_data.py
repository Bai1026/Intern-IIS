'''
This file change the dataset for input format of the Graphormer
The format woullb be like:
{"edge_index": [[0, 1], [1, 2]], "edge_attr": [[0], [0]], "y": ["0"], "num_nodes": 3, "node_feat": [[790564, 11, 724074]]}
where the unique ids are put in the node_feat
and all the node are 0 to 1 to 2, which is needed for Graphormer's input format
'''

import json

def process_graph(graph):
    node_feat = [[int(graph["edge_index"][0][0]), int(graph["edge_index"][0][1]), int(graph["edge_index"][1][1])]]
    graph["node_feat"] = node_feat
    graph["edge_index"] = [[0, 1], [1, 2]]
    return graph


# input_path = "./new_data.jsonl"
input_path = "./Labeled_data_final.jsonl"
# input_path = "/workdir/home/bai/data_processing/new_data.jsonl"

with open(input_path, "r") as f:
    lines = f.readlines()

processed_graphs = [process_graph(json.loads(line.strip())) for line in lines]

with open("processed_data.jsonl", "w") as f:
    for graph in processed_graphs:
        json.dump(graph, f)
        f.write("\n")
