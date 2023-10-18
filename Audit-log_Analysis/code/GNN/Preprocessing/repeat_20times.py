import json
from tqdm import tqdm

# 讀取 triplets_1.txt 中的標籤到一個列表中
with open('triplets_1.txt', 'r') as f:
    labels_to_augment = [int(line.strip()) for line in f.readlines()]

file_path = '../data_new/exp3/training_data_repeat/transR_50'

with open(f"{file_path}/train.jsonl", 'r') as input_file, open(f"{file_path}/repeat_train_320.jsonl", 'w') as output_file:
    count = 0
    for line in tqdm(input_file, desc="Processing", position=0, leave=True):
        data = json.loads(line.strip())
        labels = data['labels']  # 改成 'labels' 來匹配你的文件格式

        if any(label in labels_to_augment for label in labels):
            for _ in range(320):  # 更改這個數字以控制擴增的倍數
                output_file.write(json.dumps(data) + '\n')
                count += 1
        else:
            output_file.write(json.dumps(data) + '\n')
            
print(f"there's {count} of data added")
print('Data augmentation completed.')
