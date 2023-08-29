import json
from tqdm import tqdm

# 初始化三個數據集的列表
test_data = []
validation_data = []
train_data = []

embedding = 'secureBERT'
# 讀取原始數據
# with open("../data_new/test_graph/graph_without_benign_embedded.jsonl", "r") as f:
# with open("../data_new/graph/transE_50_embedded.jsonl", "r") as f:
with open(f"../data_new/graph/{embedding}_embedded.jsonl", "r") as f:
    lines = f.readlines()

# 假設每個 label 有 1000 個數據
data_per_label = 1000

# 分割數據
for i in tqdm(range(0, len(lines), data_per_label)):
    # 取出當前 label 的所有數據
    current_label_data = lines[i:i+data_per_label]
    
    # 分割為 test, validation, train
    test_data.extend(current_label_data[0:100])
    validation_data.extend(current_label_data[100:200])
    train_data.extend(current_label_data[200:1000])

# 寫入分割後的數據到對應的文件
with open(f"../data_new/training_data/{embedding}/test.jsonl", "w") as f:
    f.writelines(test_data)

with open(f"../data_new/training_data/{embedding}/valid.jsonl", "w") as f:
    f.writelines(validation_data)

with open(f"../data_new/training_data/{embedding}/train.jsonl", "w") as f:
    f.writelines(train_data)
