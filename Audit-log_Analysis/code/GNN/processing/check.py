import json
from tqdm import tqdm

jsonl_file_path = "./transE_50/test.jsonl"  # 替换为你的JSONL文件路径

# 逐行读取JSONL文件并统计行数
num_lines = 0
with open(jsonl_file_path, "r") as jsonl_file:

    for line in tqdm(jsonl_file):
        num_lines += 1
        # json_data = json.loads(line)  # 解析每一行的JSON数据

print(f"Number of lines in the JSONL file: {num_lines}")
