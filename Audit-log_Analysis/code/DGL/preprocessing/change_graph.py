import json

# Load data
data = []
with open("../data/remaining_data/train_test.jsonl", "r") as f:
# with open("../data/test.jsonl", "r") as f:
    for line in f:        
        data.append(json.loads(line.strip()))

# Helper function to convert data format
def transform_subgraphs(subgraphs):
    nodes = []
    edges = []
    edge_attrs = []
    
    for subgraph in subgraphs:
        if subgraph["node_feat"][0][0] not in nodes:
            nodes.append(subgraph["node_feat"][0][0])
        if subgraph["node_feat"][2][0] not in nodes:
            nodes.append(subgraph["node_feat"][2][0])
            
        source_idx = nodes.index(subgraph["node_feat"][0][0])
        target_idx = nodes.index(subgraph["node_feat"][2][0])
        edges.append([source_idx, target_idx])
        
        edge_attrs.append(subgraph["node_feat"][1][0])
    
    # Convert lists to required format
    edges = list(zip(*edges))
    return {
        "label": subgraphs[0]["y"][0],
        "num_nodes": len(nodes),
        "node_feat": nodes,
        "edge_attr": edge_attrs,
        "edge_index": edges
    }

# Group subgraphs by 'y'
grouped_data = {}
for item in data:
    y = item["y"][0]

    # if y == 0 or y == 76 or y == 92: continue

    if y not in grouped_data:
        grouped_data[y] = []

    grouped_data[y].append(item)

# Transform each group
result = [transform_subgraphs(grouped_data[key]) for key in grouped_data]

# Save the transformed data
# with open("../data/remaining_transformed_data_benign.jsonl", "w") as f:
with open("../data/remaining_data/transformed_train.jsonl", "w") as f:
# with open("../data/test_out.jsonl", "w") as f:
    for item in result:
        f.write(json.dumps(item) + "\n")
