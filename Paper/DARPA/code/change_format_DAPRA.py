'''
This is the file to change the original DARPA data(json file) to the data we can used(txt file)
The format would be: source, destination, relation, label

For single file(2GB), it takes about 5 hours to handle it.
'''

import os
import json
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
import glob


# for recording the processing process
import datetime
now = datetime.datetime.now()
formatted_time = now.strftime("%m%d_%H:%M")
log_file_path = f"./log_message/{formatted_time}_change_format.log"

def add_log_msg(msg, log_file_path=log_file_path):
    with open(log_file_path, 'a') as f:
        f.write(f'{datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}# {msg}\n')
    print(f'{datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}# {msg}')
print(log_file_path)


# for checking the time and add in the log file
last_log_time = datetime.datetime.now()
def should_log():
    global last_log_time
    current_time = datetime.datetime.now()
    if (current_time - last_log_time).total_seconds() >= 60:  # 檢查是否已經過去了3600秒（即一小時）
        last_log_time = current_time
        return True
    return False

# Preprocessing 
uuid_encoder = LabelEncoder()
event_encoder = LabelEncoder()
uuids = set()
events = set()

input_folder_path = '../data_new/DARPA/source_data'
output_data_path = '../data_new/DARPA/before_embedding/'

json_files = glob.glob(os.path.join(input_folder_path, '*.json'))
add_log_msg(f"we got {len(json_files)} files here")


for file_path in tqdm(json_files):
    add_log_msg(f"Handling: {file_path} now")
    
    if should_log():
        add_log_msg(f"Current progress: Handling {file_path}")

    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                uuids.add(data['subj']['uuid'])
                uuids.add(data['obj']['uuid'])
                events.add(data['relation'])
            except json.JSONDecodeError as e:
                add_log_msg(f"JSON got error: {e}")
                continue

uuid_encoder.fit(list(uuids))
event_encoder.fit(list(events))

count = 0
with open(output_data_path + 'uuid_mapping.txt', 'w') as file:
    add_log_msg(f"Handling: {output_data_path + 'uuid_mapping.txt'} now")

    for uuid in tqdm(uuids):
        count += 1
        if count % 1000 == 0:
            add_log_msg("still handing uuid")
        if should_log():
            add_log_msg(f"Current progress: Handling {file_path}")
        number = uuid_encoder.transform([uuid])[0]
        file.write(f"{uuid}: {number}\n")
    add_log_msg(f"uuid saved at: {output_data_path + 'uuid_mapping.txt'}")
    

with open(output_data_path + 'event_mapping.txt', 'w') as file:
    add_log_msg(f"Handling: {output_data_path + 'event_mapping.txt'} now")

    for event in tqdm(events):
        if should_log():
            add_log_msg(f"Current progress: Handling {file_path}")
        number = event_encoder.transform([event])[0]
        file.write(f"{event}: {number}\n")
    add_log_msg(f"event_mapping saved at{output_data_path + 'event_mapping.txt'}")


with open(output_data_path + 'output.txt', 'w') as out_file:
    add_log_msg(f"Handling: {output_data_path + 'output.txt'} now")


    for file_path in tqdm(json_files):
        with open(file_path, 'r') as file:

            for line in file:
                if should_log():
                    add_log_msg(f"Current progress: Handling {file_path}")

                try:
                    data = json.loads(line)
                    subj_num = uuid_encoder.transform([data['subj']['uuid']])[0]
                    obj_num = uuid_encoder.transform([data['obj']['uuid']])[0]
                    rel_num = event_encoder.transform([data['relation']])[0]
                    label = 'b' if data['label'] == 'benign' else 'a'

                    out_file.write(f"{subj_num} {obj_num} {rel_num} {label}\n")
                except json.JSONDecodeError:
                    continue
    add_log_msg(f"output.txt saved at: {output_data_path + 'output.txt'}")

# # This is the file to change the original DARPA data(json file) to the daata we can used(txt file)
# # The format would be: source, destination, relation, label

# # For single file(2GB), it takes about 5 hours to handle it.

# '''
# This is the file to change the original DARPA data(json file) to the daata we can used(txt file)
# The format would be: source, destination, relation, label

# For single file(2GB), it takes about 5 hours to handle it.
# '''

# import os
# import json
# from sklearn.preprocessing import LabelEncoder
# from tqdm import tqdm
# import glob


# # for recording the processing process
# import datetime
# now = datetime.datetime.now()
# formatted_time = now.strftime("%m%d_%H:%M")
# log_file_path = f"./log_message/{formatted_time}_change_format.log"

# def add_log_msg(msg, log_file_path=log_file_path):
#     with open(log_file_path, 'a') as f:
#         f.write(f'{datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}# {msg}\n')
#     print(f'{datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}# {msg}')
# print(log_file_path)


# # for checking the time and add in the log file
# last_log_time = datetime.datetime.now()
# def should_log(tqdm_object=None):
#     global last_log_time
#     current_time = datetime.datetime.now()
#     if (current_time - last_log_time).total_seconds() >= 60:  # 檢查是否已經過去了60秒
#         last_log_time = current_time
#         if tqdm_object:
#             remaining = tqdm_object.format_dict['remaining']
#             msg = f"Current progress: {tqdm_object.n}/{tqdm_object.total}, Time left: {remaining}"
#             add_log_msg(msg)
#         return True
#     return False


# # Preprocessing 
# uuid_encoder = LabelEncoder()
# event_encoder = LabelEncoder()
# uuids = set()
# events = set()

# input_folder_path = '../data_new/DARPA/source_data'
# output_data_path = '../data_new/DARPA/before_embedding/'

# json_files = glob.glob(os.path.join(input_folder_path, '*.json'))
# add_log_msg(f"we got {len(json_files)} files here")


# for file_path in tqdm(json_files, desc="Processing JSON files"):
#     add_log_msg(f"Handling: {file_path} now")
    
#     if should_log():
#         add_log_msg(f"Current progress: Handling {file_path}")

#     with open(file_path, 'r') as file:
#         for line in file:
#             try:
#                 data = json.loads(line)
#                 uuids.add(data['subj']['uuid'])
#                 uuids.add(data['obj']['uuid'])
#                 events.add(data['relation'])
#             except json.JSONDecodeError as e:
#                 add_log_msg(f"JSON got error: {e}")
#                 continue

# uuid_encoder.fit(list(uuids))
# event_encoder.fit(list(events))

# count = 0
# with open(output_data_path + 'uuid_mapping.txt', 'w') as file:
#     add_log_msg(f"Handling: {output_data_path + 'uuid_mapping.txt'} now")

#     tqdm_object = tqdm(uuids, desc="Processing uuids files")
#     # for uuid in tqdm(uuids, desc="Processing uuids files"):
#     for uuid in tqdm_object:
#         count += 1
#         if count % 100 == 0: add_log_msg("still going")
#         # if should_log():
#         #     add_log_msg(f"Current progress: Handling {file_path}")
#         if should_log(tqdm_object=tqdm_object):
#             pass
        
#         number = uuid_encoder.transform([uuid])[0]
#         file.write(f"{uuid}: {number}\n")
#     add_log_msg(f"uuid saved at: {output_data_path + 'uuid_mapping.txt'}")
    

# with open(output_data_path + 'event_mapping.txt', 'w') as file:
#     add_log_msg(f"Handling: {output_data_path + 'event_mapping.txt'} now")

#     tqdm_object = tqdm(events, desc="Processing events files")
#     # for event in tqdm(events, desc="Processing events files"):
#     for event in tqdm_object:
#         if should_log(tqdm_object=tqdm_object):
#             pass
#         number = event_encoder.transform([event])[0]
#         file.write(f"{event}: {number}\n")
#     add_log_msg(f"event_mapping saved at{output_data_path + 'event_mapping.txt'}")


# with open(output_data_path + 'output.txt', 'w') as out_file:
#     add_log_msg(f"Handling: {output_data_path + 'output.txt'} now")

#     tqdm_object = tqdm(json_files, desc="Processing output files")
#     for file_path in tqdm_object:
#         with open(file_path, 'r') as file:

#             for line in file:
#                 if should_log(tqdm_object=tqdm_object):
#                     # 日誌已在 should_log 函數內部被記錄，無需額外操作
#                     pass

#                 try:
#                     data = json.loads(line)
#                     subj_num = uuid_encoder.transform([data['subj']['uuid']])[0]
#                     obj_num = uuid_encoder.transform([data['obj']['uuid']])[0]
#                     rel_num = event_encoder.transform([data['relation']])[0]
#                     label = 'b' if data['label'] == 'benign' else 'a'

#                     out_file.write(f"{subj_num} {obj_num} {rel_num} {label}\n")
#                 except json.JSONDecodeError:
#                     continue
#     add_log_msg(f"output.txt saved at: {output_data_path + 'output.txt'}")




# import json
# from sklearn.preprocessing import LabelEncoder
# from tqdm import tqdm

# # 初始化 LabelEncoder 和集合用于收集唯一的 UUID 和事件类型
# uuid_encoder = LabelEncoder()
# event_encoder = LabelEncoder()
# uuids = set()
# events = set()

# input_data_path = '../data_new/DARPA/test.json'
# output_data_path = '../data_new/DARPA/before_embedding/'


# count = 0
# with open(input_data_path, 'r') as file:
#     add_log_msg('in')
#     for line in tqdm(file):
#         count += 1
#         # try:
#         #     data = json.loads(line)
#         #     uuids.add(data['subj']['uuid'])
#         #     uuids.add(data['obj']['uuid'])
#         #     events.add(data['relation'])
#         # except json.JSONDecodeError as e:
#         #     add_log_msg(f"JSON 解析错误：{e}")
#         #     add_log_msg("有问题的行内容：", line)
#         #     continue  # 跳过有问题的行

#         if count == 716907:
#             break
#         else:
#             data = json.loads(line)
#             uuids.add(data['subj']['uuid'])
#             uuids.add(data['obj']['uuid'])
#             events.add(data['relation'])

#     add_log_msg('end')  # 这里应该会执行

# # add_log_msg(uuids)
# # 对 UUID 和事件类型进行编码
# uuid_encoder.fit(list(uuids))
# event_encoder.fit(list(events))

# # 将映射关系写入到文件中
# with open(output_data_path + 'uuid_mapping.txt', 'w') as file:
#     # add_log_msg('in 1')
#     for uuid in tqdm(uuids):
#         number = uuid_encoder.transform([uuid])[0]
#         file.write(f"{uuid}: {number}\n")
#     add_log_msg(output_data_path + 'uuid_mapping.txt')

# with open(output_data_path + 'event_mapping.txt', 'w') as file:
#     add_log_msg('in 2')
#     for event in tqdm(events):
#         number = event_encoder.transform([event])[0]
#         file.write(f"{event}: {number}\n")
#     add_log_msg(output_data_path + 'event_mapping.txt')

# # 使用映射转换原始数据
# with open(input_data_path, 'r') as file, open(output_data_path + 'output.txt', 'w') as out_file:
#     add_log_msg('START!')
#     for line in tqdm(file):
#         try:
#             data = json.loads(line)
#         except json.JSONDecodeError as e:
#             add_log_msg(f"JSON 解析错误：{e}")
#             add_log_msg(line)
#             continue 

#         subj_num = uuid_encoder.transform([data['subj']['uuid']])[0]
#         obj_num = uuid_encoder.transform([data['obj']['uuid']])[0]
#         rel_num = event_encoder.transform([data['relation']])[0]
#         label = 'b' if data['label'] == 'benign' else 'a'

#         out_file.write(f"{subj_num} {obj_num} {rel_num} {label}\n")
#     add_log_msg(output_data_path + 'output.txt')



