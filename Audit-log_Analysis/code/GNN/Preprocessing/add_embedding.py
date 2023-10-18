# import os
# import json
# from tqdm import tqdm

# with open("../data_new/embedding/transR_50.vec.json", "r") as f:
#     embeddings = json.load(f)
    
# # print("Keys in the embeddings:", embeddings.keys())

# ent_embeddings = embeddings["ent_embeddings.weight"]
# edge_embeddings = embeddings["rel_embeddings.weight"]  # Assuming the key is edge_embeddings.weight


# # input_filenames = ["../data/test/transformed_test.jsonl", "../data/test/transformed_train.jsonl", "../data/test/transformed_valid.jsonl"]
# input_filenames = ["../data_new/graph/graph_without_benign.jsonl"]

# for input_filename in tqdm(input_filenames):
#     base, ext = os.path.splitext(input_filename)

#     output_filename = f"{base}_embedded{ext}"
#     # output_filename = "../data_new/test_graph/" + new_filename
    
#     with open(input_filename, "r") as f, open(output_filename, "w") as out_file:
        
#         for line in tqdm(f):
#             data = json.loads(line.strip())

#             # Replace node_feat and edge_attr with embeddings
#             data["node_feat"] = [ent_embeddings[node_id] for node_id in data["node_feat"]]
#             data["edge_attr"] = [edge_embeddings[edge_id] for edge_id in data["edge_attr"]]

#             # Convert the data back to a JSON string and write to the output file
#             out_file.write(json.dumps(data) + '\n')

import os
import json
from tqdm import tqdm

# embedding_files = [
#     "../data_new/embedding/transE_100.vec.json", "../data_new/embedding/transE_150.vec.json", "../data_new/embedding/transE_50.vec.json",
#     "../data_new/embedding/transH_100.vec.json", "../data_new/embedding/transH_150.vec.json", "../data_new/embedding/transH_50.vec.json"
# ]

embedding_files = ["../data_new/embedding/transE_150.vec.json"]

embeddings = {}
for embedding_file in tqdm(embedding_files):
    print("hi")
    with open(embedding_file, "r") as f:
        print("in")
        embeddings[embedding_file] = json.load(f)
        print("finish")

# 输入文件列表
# input_filenames = ["../data_new/graph/graph_without_benign.jsonl"]
input_filenames = ["../data_new/exp3/graph/graph_exp3.jsonl"]

for input_filename in tqdm(input_filenames):
    print("Start!")
    base, ext = os.path.splitext(input_filename)
    
    with open(input_filename, "r") as f:
        input_data = list(f)

    for embedding_key, embedding_data in tqdm(embeddings.items()):
        output_filename = f"{embedding_key.replace('.json', '_embedded').replace('.vec', '')}{ext}"
        print(output_filename)

        with open(output_filename, "w") as out_file:
            ent_embeddings = embedding_data["ent_embeddings.weight"]
            edge_embeddings = embedding_data["rel_embeddings.weight"]

            for line, data in tqdm(zip(input_data, input_data)):
                data = json.loads(data.strip())

                # Replace node_feat and edge_attr with embeddings
                data["node_feat"] = [ent_embeddings[node_id] for node_id in data["node_feat"]]
                data["edge_attr"] = [edge_embeddings[edge_id] for edge_id in data["edge_attr"]]

                # Convert the data back to a JSON string and write to the output file
                out_file.write(json.dumps(data) + '\n')
