# Can only use in multi-files case
import os
import json

# file_path = "../test.jsonl"
file_paths = ["../data_v2/train.jsonl", "../data_v2/test.jsonl", "../data_v2/valid.jsonl"]
# file_paths = "../data_v2/processed_data.jsonl"

# 確保 file_path 是一個文件路徑
for file_path in file_paths:
    if os.path.isfile(file_path):
        # 打開 JSONL 文件進行讀取
        with open(file_path, "r") as file:
            processed_data = []
            for line in file:
                # 解析 JSON 字串成 Python 物件
                data = json.loads(line)
                # 在這裡進行對 data 的處理
                data['node_feat'] = [[item] for item in data['node_feat'][0]]
                # print(data)
                processed_data.append(data)

            output_file_path = file_path.replace(".jsonl", "_processed_v2.jsonl")
            print(output_file_path)
            with open(output_file_path, "w") as output_file:
                for data in processed_data:
                    json.dump(data, output_file)
                    output_file.write("\n")
    else:
        print(f"Error: {file_path} not valid")



# # ==================== For single file case ====================
# import os
# import json

# file_path = "../data_v2/processed_data.jsonl"

# # 確保 file_path 是一個文件路徑
# if os.path.isfile(file_path):
#     # 打開 JSONL 文件進行讀取
#     with open(file_path, "r") as file:
#         processed_data = []
#         for line in file:
#             # 解析 JSON 字串成 Python 物件
#             data = json.loads(line)
#             # 在這裡進行對 data 的處理
#             data['node_feat'] = [[item] for item in data['node_feat'][0]]
#             processed_data.append(data)

#         output_file_path = file_path.replace(".jsonl", "_processed_v2.jsonl")
#         print(output_file_path)
#         with open(output_file_path, "w") as output_file:
#             for data in processed_data:
#                 json.dump(data, output_file)
#                 output_file.write("\n")
# else:
#     print(f"Error: {file_path} not valid")
