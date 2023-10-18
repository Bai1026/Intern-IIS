import json
from tqdm import tqdm

files = ['transE_50', 'transE_100', 'transE_150', 'transH_50', 'transH_100', 'transH_150', 'transR_50', 'secureBERT']

for file in tqdm(files):
    file1 = f"../data_new/graph/benign/{file}_embedded.jsonl"
    data1 = []

    with open(file1, 'r') as f:
        for line in f:
            data1.append(json.loads(line))

    file2 = f"../data_new/graph/without_benign/{file}_embedded.jsonl"
    data2 = []

    with open(file2, 'r') as f:
        for line in f:
            data2.append(json.loads(line))

    combined_data = data1 + data2

    output_file = f"../data_new/graph/with_benign/{file}_embedded.jsonl"
    print(output_file)

    with open(output_file, 'w') as f:
        for item in combined_data:
            f.write(json.dumps(item) + '\n')
