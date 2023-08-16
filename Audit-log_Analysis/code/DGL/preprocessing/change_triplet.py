import json

# 讀取原始的jsonl文件
# with open('../data/remaining_data/test_test.jsonl', 'r') as infile:
with open('../data/remaining_data/validation_test.jsonl', 'r') as infile:
    data = [json.loads(line) for line in infile]

# 格式轉換
transformed_data = []
for item in data:
    new_item = {
        "label": item["y"][0],
        "num_nodes": 2,
        "node_feat": [item["node_feat"][0][0], item["node_feat"][2][0]],
        "edge_attr": [item["node_feat"][1][0]],
        "edge_index": [[0], [1]]
    }
    transformed_data.append(new_item)

# 寫入轉換後的jsonl文件
# with open('../data/test/transformed_test.jsonl', 'w') as outfile:
with open('../data/test/transformed_valid.jsonl', 'w') as outfile:
    for item in transformed_data:
        json.dump(item, outfile)
        outfile.write('\n')
