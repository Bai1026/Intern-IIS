'''
Just change the name of the dataset's column name
'''
import json
import pandas as pd

input_file = 'labeled_data_final.jsonl'
output_file = 'Labeled_data_final.jsonl'

# 讀取JSON Lines檔案到DataFrame
df = pd.read_json(input_file, lines=True)

# 將"label"轉換為字串
# df['label'] = df['label'].apply(lambda x: x[0])  # 將包含單一元素的串列轉換成單一值
# df['y'] = df.pop('label')

df['label'] = df['label'].apply(lambda x: [x[0]])  # 將包含單一元素的串列轉換成單一值的列表
df.rename(columns={'label': 'y'}, inplace=True)

# 將DataFrame輸出為JSON Lines檔案
df.to_json(output_file, orient='records', lines=True)


# import json
# import pandas as pd

# input_file = 'labeled_data_final.jsonl'
# output_file = 'Labeled_data_final.jsonl'

# df = pd.read_json(input_file, lines=True)

# # Just change the index if want to modify the name
# # df['edge_attr'] = df.pop('edge_feat')
# df['y'] = df.pop('label')
# # df['num_nodes'] = df.pop('node_num')

# df.to_json(output_file, orient='records', lines=True)
