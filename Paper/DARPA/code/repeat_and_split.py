import json
from tqdm import tqdm

def read_jsonl_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [json.loads(line) for line in tqdm(lines, desc='Reading JSONL', unit='lines')]

def write_jsonl_file(data, file_path):
    with open(file_path, 'w') as file:
        for item in tqdm(data, desc='Writing JSONL', unit='items'):
            file.write(json.dumps(item) + '\n')

def repeat_and_split_data(file_path, repeat_times=1, train_ratio=0.8, valid_ratio=0.1):
    data = read_jsonl_file(file_path)
    repeated_data = data * repeat_times

    train_size = int(len(repeated_data) * train_ratio)
    valid_size = int(len(repeated_data) * valid_ratio)

    train_data = repeated_data[:train_size]
    valid_data = repeated_data[train_size:train_size + valid_size]
    test_data = repeated_data[train_size + valid_size:]

    return train_data, valid_data, test_data

# Replace with your JSONL file path
file_path = '/workdir/home/bai/Euni_HO_modified/data/source_data/secureBERT_150_embedded(edge768).jsonl'
train_data, valid_data, test_data = repeat_and_split_data(file_path)

# Save the divided data
write_jsonl_file(train_data, '/workdir/home/bai/Euni_HO_modified/data/training_data/secureBERT_150/train.jsonl')
write_jsonl_file(valid_data, '/workdir/home/bai/Euni_HO_modified/data/training_data/secureBERT_150/valid.jsonl')
write_jsonl_file(test_data, '/workdir/home/bai/Euni_HO_modified/data/training_data/secureBERT_150/test.jsonl')


# import json
# from tqdm import tqdm 

# def read_jsonl_file(file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#     return [json.loads(line) for line in tqdm(lines)]

# def write_jsonl_file(data, file_path):
#     with open(file_path, 'w') as file:
#         for item in tqdm(data):
#             file.write(json.dumps(item) + '\n')

# def repeat_and_split_data(file_path, repeat_times=10, train_ratio=0.8, valid_ratio=0.1):
#     data = read_jsonl_file(file_path)
#     repeated_data = data * repeat_times

#     train_size = int(len(repeated_data) * train_ratio)
#     valid_size = int(len(repeated_data) * valid_ratio)

#     train_data = repeated_data[:train_size]
#     valid_data = repeated_data[train_size:train_size + valid_size]
#     test_data = repeated_data[train_size + valid_size:]

#     return train_data, valid_data, test_data

# # 替换为您的JSONL文件路径
# file_path = '/workdir/home/bai/Euni_HO_modified/data/training_data/secureBERT_150_embedded(edge768).jsonl'
# train_data, valid_data, test_data = repeat_and_split_data(file_path)

# # 保存划分后的数据
# write_jsonl_file(train_data, '/workdir/home/bai/Euni_HO_modified/data/training_data/secureBERT_150/train.jsonl')
# write_jsonl_file(valid_data, '/workdir/home/bai/Euni_HO_modified/data/training_data/secureBERT_150/valid.jsonl')
# write_jsonl_file(test_data, '/workdir/home/bai/Euni_HO_modified/data/training_data/secureBERT_150/test.jsonl')

