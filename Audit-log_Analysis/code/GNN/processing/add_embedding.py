# import os
# import json
# from tqdm import tqdm

# with open("../data_new/source_data/embedding/transR_50.vec.json", "r") as f:
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

# import os
# import json
# from tqdm import tqdm

# # 读取所有嵌入映射 JSON 文件
# embedding_files = [
#     "../data_new/source_data/embedding/transE_100.vec.json", "../data_new/source_data/embedding/transE_150.vec.json", "../data_new/source_data/embedding/transE_50.vec.json",
#     "../data_new/source_data/embedding/transH_100.vec.json", "../data_new/source_data/embedding/transH_150.vec.json", "../data_new/source_data/embedding/transH_50.vec.json",
#     "../data_new/source_data/embedding/transR_50.vec.json"
# ]

# embeddings = {}
# for embedding_file in tqdm(embedding_files):
#     with open(embedding_file, "r") as f:
#         embeddings[embedding_file] = json.load(f)

# # 输入文件列表
# input_filenames = ["../data_new/graph/graph_without_benign.jsonl"]

# for input_filename in tqdm(input_filenames):
#     print("Start!")
#     base, ext = os.path.splitext(input_filename)
    
#     with open(input_filename, "r") as f:
#         input_data = list(f)

#     for embedding_key, embedding_data in tqdm(embeddings.items()):
#         output_filename = f"{embedding_key.replace('.json', '_embedded').replace('.vec', '')}{ext}"
#         print(output_filename)

#         with open(output_filename, "w") as out_file:
#             ent_embeddings = embedding_data["ent_embeddings.weight"]
#             edge_embeddings = embedding_data["rel_embeddings.weight"]

#             for line, data in tqdm(zip(input_data, input_data)):
#                 data = json.loads(data.strip())

#                 # Replace node_feat and edge_attr with embeddings
#                 data["node_feat"] = [ent_embeddings[node_id] for node_id in data["node_feat"]]
#                 data["edge_attr"] = [edge_embeddings[edge_id] for edge_id in data["edge_attr"]]

#                 # Convert the data back to a JSON string and write to the output file
#                 out_file.write(json.dumps(data) + '\n')

import os
import json
import numpy as np
from tqdm import tqdm
from sklearn.decomposition import PCA

# Load embedding function
def load_embedding(input_embedding_name, model):
    if model.startswith('trans'):
        with open(input_embedding_name) as f:
            data = json.load(f)
        ent_embeddings = np.array(data['ent_embeddings.weight'])
        rel_embeddings = np.array(data['rel_embeddings.weight'])
        return ent_embeddings, rel_embeddings
    
    elif model == 'secureBERT':
        ent_embeddings = np.empty((0, 768), dtype=np.float32)
        for filename in sorted(os.listdir(input_embedding_name)):
            print(filename)

            if not filename.startswith('embeddings_chunk'):
                continue

            embedding = np.load(f'{input_embedding_name}/{filename}')

            print(ent_embeddings.shape, embedding.shape)

            ent_embeddings = np.concatenate((ent_embeddings, embedding), axis=0)
            print(filename, ent_embeddings.shape)

        print(f'Reducing entity embedding to ({DIM},)')
        print(ent_embeddings.shape, '->', end=' ')
        pca = PCA(n_components=DIM)
        ent_embeddings = pca.fit_transform(ent_embeddings)
        print(ent_embeddings.shape)

        rel_embeddings = np.load(f'{input_embedding_name}/relation.npy')
        print(f'Reducing relation embedding to ({len(rel_embeddings)},)')
        print(rel_embeddings.shape, '->', end=' ')
        pca = PCA(n_components=len(rel_embeddings))
        rel_embeddings = pca.fit_transform(rel_embeddings)
        print(rel_embeddings.shape)
        return ent_embeddings, rel_embeddings
    else:
        print('Error!!')
        return None
    

embedding_files = ["../data_new/source_data/embedding/secureBERT"]
model = 'secureBERT'
DIM = 250

# 输入文件列表
input_filenames = ["../data_new/graph/graph_without_benign.jsonl"]

for input_filename in tqdm(input_filenames):
    print("Start!")
    base, ext = os.path.splitext(input_filename)
    
    with open(input_filename, "r") as f:
        input_data = list(f)

    for embedding_file in tqdm(embedding_files):
        output_filename = f"{embedding_file.replace('.json', '_embedded').replace('.vec', '')}{ext}"
        print(output_filename)

        with open(output_filename, "w") as out_file:
            model = embedding_file.split('/')[-1].split('_')[0]
            ent_embeddings, rel_embeddings = load_embedding(embedding_file, model)
            # ...

            for line, data in tqdm(zip(input_data, input_data)):
                data = json.loads(data.strip())

                # Replace node_feat and edge_attr with embeddings
                data["node_feat"] = [ent_embeddings[node_id].tolist() if model == 'secureBERT' else ent_embeddings[node_id] for node_id in data["node_feat"]]
                data["edge_attr"] = [rel_embeddings[edge_id].tolist() for edge_id in data["edge_attr"]]

                # Convert the data back to a JSON string and write to the output file
                out_file.write(json.dumps(data) + '\n')

            # for line, data in tqdm(zip(input_data, input_data)):
            #     data = json.loads(data.strip())

            #     # Replace node_feat and edge_attr with embeddings
            #     data["node_feat"] = [ent_embeddings[node_id] for node_id in data["node_feat"]]
            #     data["edge_attr"] = [rel_embeddings[edge_id] for edge_id in data["edge_attr"]]

            #     # Convert the data back to a JSON string and write to the output file
            #     out_file.write(json.dumps(data) + '\n')
