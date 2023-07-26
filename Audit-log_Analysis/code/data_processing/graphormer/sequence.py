'''
This file help me to convert the jsonl file to the format of the OGB-molhiv format
And I've put the dataset on the HuggingFace
URL: https://huggingface.co/VincentPai
'''

import json
import pandas as pd

jsonl_path = "/workdir/home/bai/Data_Graphormer/labeled_data.jsonl"

# 读取JSON Lines文件
with open(jsonl_path, 'r') as f:
    data = [json.loads(line) for line in f]

# 调整数据结构
for item in data:
    # 转换node_num为int64类型
    item['node_num'] = int(item['node_num'])

# 创建DataFrame
df = pd.DataFrame(data)

# 重新排列列的顺序
df = df[['edge_index', 'edge_feat', 'label', 'node_num', 'node_feat']]

# 将DataFrame保存为JSON Lines文件
df.to_json('new_data.jsonl', orient='records', lines=True)

