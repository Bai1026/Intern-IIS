import json

# 讀取映射文件並建立一個字典
mapping = {}
with open('../data_v2/label_encoding_mapping.txt', 'r') as f:
    for line in f:
        k, v = line.strip().split(':')
        mapping[k.strip()] = int(v.strip())

# 讀取並更新jsonl文件
jsonl_data = []
with open('../data_v2/processed_data_v2.jsonl', 'r') as f:
    for line in f:
        line_data = json.loads(line)
        key = line_data['y'][0]
        if key in mapping:
            line_data['y'] = [mapping[key]]
        jsonl_data.append(line_data)

# 將更新後的數據寫回jsonl文件
with open('../data_v2/processed_encoded_data.jsonl', 'w') as f:
    for item in jsonl_data:
        f.write(json.dumps(item) + '\n')
