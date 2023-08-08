import json

# 1. Load embeddings
with open("../data/transR_50.vec.json", "r") as f:
    embeddings = json.load(f)
    
# Check the keys in the embeddings
print("Keys in the embeddings:", embeddings.keys())

# Get the entity and edge embeddings
ent_embeddings = embeddings["ent_embeddings.weight"]
edge_embeddings = embeddings["rel_embeddings.weight"]  # Assuming the key is edge_embeddings.weight

# 2. Read and process the .jsonl file
# Assuming you have already loaded the embeddings into ent_embeddings and edge_embeddings...
# input_filename = "../data/remaining_transformed_data_v2.jsonl"
input_filename = "../data/merged_transformed_data.jsonl"
output_filename = "../data/embedded_merged_data.jsonl"

# map the dgl node_id to the real node_id
with open(input_filename, "r") as f:
    label_0_count = 1

    for line in f:
        graph = json.loads(line.strip())
        label = graph["label"]
        
        # If label is 0, update filename with the count
        if label == 0:
            mapping_filename = f"label-{label}.{label_0_count}.txt"
            label_0_count += 1
        else:
            mapping_filename = f"label-{label}.txt"

        # 為每一個label創建一個映射文件
        with open(mapping_filename, "w") as out_file:
            for idx, node_id in enumerate(graph["node_feat"]):
                out_file.write(f"{idx}: {node_id}\n")


# with open(input_filename, "r") as f, open(output_filename, "w") as out_file:
#     for line in f:
#         data = json.loads(line.strip())

#         # Replace node_feat and edge_attr with embeddings
#         data["node_feat"] = [ent_embeddings[node_id] for node_id in data["node_feat"]]
#         data["edge_attr"] = [edge_embeddings[edge_id] for edge_id in data["edge_attr"]]

#         # Convert the data back to a JSON string and write to the output file
#         out_file.write(json.dumps(data) + '\n')

