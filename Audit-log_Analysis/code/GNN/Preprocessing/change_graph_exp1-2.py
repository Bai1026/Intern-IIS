import os
import json
from tqdm import tqdm

def process_file(file_path, label, count):
    # if count == 14: return
    with open(file_path, "r") as f:
        lines = f.readlines()

    nodes = set()
    edges = []
    edge_attrs = []
    # label = []
    
    for line in lines:
        parts = line.strip().split()
        source_node = int(parts[0])
        dest_node = int(parts[1])
        edge_id = int(parts[2])
        
        nodes.add(source_node)
        nodes.add(dest_node)
        edges.append([source_node, dest_node])
        edge_attrs.append(edge_id)
    
    nodes = list(nodes)
    edges = [[nodes.index(edge[0]), nodes.index(edge[1])] for edge in edges]
    
    # Convert lists to required format
    edges = list(zip(*edges))
    
    return {
        "label": label,
        "num_nodes": len(nodes),
        "node_feat": nodes,
        "edge_attr": edge_attrs,
        "edge_index": edges
    }

output_data = []
# folder_path = "../data_new/source_data/4_extended_APG_bai"
# folder_path = "../data_new/source_data/4"
folder_path = "../data_new/exp3/source_data/test"
folder_names = os.listdir(folder_path)

for folder_name in folder_names:
    # if folder_name == "65" or folder_name == "20230817_readme.md": 
    #     continue # skip these folders/files
    count = 0
    
    folder_path_inside = os.path.join(folder_path, folder_name)
    files = os.listdir(folder_path_inside)

    for file_name in tqdm(files):
        print(f"in to {count}")
        # if count == 9: continue
        if file_name.endswith(".txt"):
            
            file_path = os.path.join(folder_path_inside, file_name)
            print("hi")
            data = process_file(file_path, int(folder_name), count)
            print("hi2")
            output_data.append(data)
            # if count == 912: print(data)
            print(f"finish: {count}")

        count += 1
        print(data)
        # if count == 10: break
        print("out")

# with open("../data_new/test_graph/graph_without_benign.jsonl", "w") as f:
# with open("../data_new/graph/with_benign/graph_benign_test.jsonl", "w") as f:
with open("../data_new/graph/with_benign/graph_benign_test.jsonl", "a") as f:
    for item in output_data:
        f.write(json.dumps(item))
        f.write("\n")
