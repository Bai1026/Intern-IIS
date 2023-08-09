import jsonlines
import random
import os

# 設定 JSONL 文件的路徑
file_path = "../data/training_data/repeated_embedded_merged_data.jsonl"  # 自行替換成你的 JSONL 文件路徑

# 讀取 JSONL 文件中的所有圖形
all_graphs = []
with jsonlines.open(file_path) as reader:
    for item in reader:
        all_graphs.append(item)

# 打亂數據集順序
random.shuffle(all_graphs)

num_samples = len(all_graphs)
num_train = int(0.6 * num_samples)  # 60% 訓練集
num_val = int(0.2 * num_samples)    # 20% 驗證集
num_test = num_samples - num_train - num_val  # 剩餘的測試集

# 切分數據集成訓練集、驗證集和測試集
train_graphs = all_graphs[:num_train]
val_graphs = all_graphs[num_train:num_train + num_val]
test_graphs = all_graphs[num_train + num_val:]


train_file = "../data/training_data/repeated_train.jsonl"
val_file = "../data/training_data/repeated_valid.jsonl"
test_file = "../data/training_data/repeated_test.jsonl"

with jsonlines.open(train_file, mode='w') as writer:
    for graph in train_graphs:
        writer.write(graph)

with jsonlines.open(val_file, mode='w') as writer:
    for graph in val_graphs:
        writer.write(graph)

with jsonlines.open(test_file, mode='w') as writer:
    for graph in test_graphs:
        writer.write(graph)
