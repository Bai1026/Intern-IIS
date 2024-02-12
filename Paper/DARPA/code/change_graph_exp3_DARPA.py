import os
import json
from tqdm import tqdm
import logging 

def process_data(data_lines):
    node_to_index = {}
    nodes = set()
    edges = []
    edge_attrs = []
    labels = []
    
    for line in tqdm(data_lines, desc="Processing lines"):
        try:
            parts = line.strip().split()
            source_node = int(parts[0])
            dest_node = int(parts[1])
            edge_id = int(parts[2])
            label = parts[3]  
            
            # 0 means benign, 1 means malicious
            if label == 'benign':
                label = 0
            else:
                label = 1

            nodes.add(source_node)
            nodes.add(dest_node)
            edges.append([source_node, dest_node])
            edge_attrs.append(edge_id)
            labels.append(label)
        except Exception as e:
            print(f"Error processing line: {line}\nError: {e}")
            continue
    
    for index, node in enumerate(nodes):
        node_to_index[node] = index

    edges = [[node_to_index[edge[0]], node_to_index[edge[1]]] for edge in edges]
    edges = list(zip(*edges))
    
    return {
        "labels": labels,
        "num_nodes": len(nodes),
        "node_feat": list(nodes),
        "edge_attr": edge_attrs,
        "edge_index": edges
    }


def read_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()


# folder_path = '../data_new/DARPA/before_embedding/3.10/output_graphs'

# contains 1000 folders with 400 folders with graph
folder_path = '/workdir/home/bai/Euni_HO_DARPA/data/source_data/output_graphs(200)-2'
# folder_path = '../data_new/DARPA/before_embedding/output_graphs_test'

all_graph_data = []

try:
    file_names = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    for file_name in tqdm(file_names, desc="Handling Documents: "):
        file_path = os.path.join(folder_path, file_name)
        data_lines = read_data_from_file(file_path)
        graph_data = process_data(data_lines)
        all_graph_data.append(graph_data)
except Exception as e:
    print(f"Error during processing files. Error: {e}")


output_file_path = '../data_new/DARPA/before_embedding/3.10/all_graph_data.jsonl'
# output_file_path = '/workdir/home/bai/Euni_HO_DARPA/data/3_openKE/synthesize/all_graph_data(200).jsonl'
with open(output_file_path, 'w', encoding='utf-8') as f:
    for graph_data in tqdm(all_graph_data, desc="writing into output JSONL file"):
        f.write(json.dumps(graph_data))
        f.write("\n")

print(f"all the data is saved in '{output_file_path}'")