import json
from sklearn.preprocessing import LabelEncoder

jsonl_file_path = "../data_v2/processed_data_v2.jsonl"
label_encoder = LabelEncoder()

all_y_values = []  # 用於收集所有的 "y" 值

with open(jsonl_file_path, "r") as file:
    for line in file:
        data = json.loads(line)
        y_str = data["y"][0]  # 取得y的字串值
        all_y_values.append(y_str)

# 使用 fit 方法考慮所有可能的 "y" 值
label_encoder.fit(all_y_values)

# 創建一個 dictionary 來存儲 encoding mapping
label_encoding_mapping = {}

# 將 encoding mapping 儲存到字典中
for y_str in all_y_values:
    y_encoded = label_encoder.transform([y_str])[0]
    label_encoding_mapping[y_str] = y_encoded

# 將 encoding mapping 存為 txt 檔案
mapping_output_file_path = "../data_v2/label_encoding_mapping.txt"
with open(mapping_output_file_path, "w") as mapping_output_file:
    for key, value in label_encoding_mapping.items():
        mapping_output_file.write(f"{key}: {value}\n")
