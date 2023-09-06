import os

# 讀取映射文件
mapping = {}
with open('new_mapping.txt', 'r') as file:
    for line in file:
        parts = line.strip().split(': ')
        # print(len(parts))
        if len(parts) == 2:
            filename, number = parts
            mapping[filename] = int(number)

# 資料夾的路徑
folder_path = '../data_new/exp3/source_data/without_benign'
# print(mapping)

# 遍歷資料夾
for folder_name in os.listdir(folder_path):
    folder_path_full = os.path.join(folder_path, folder_name)
    
    # 檢查是否包含"(has_benign)"，如果是，則忽略
    if '(has_benign)' in folder_name:
        folder_name = folder_name.replace("(has_benign)", "")
    
    print(folder_name)
    # 如果文件名在映射中，則進行重命名
    if folder_name in mapping:
        new_folder_name = str(mapping[folder_name])
        new_folder_path_full = os.path.join(folder_path, new_folder_name)
        os.rename(folder_path_full, new_folder_path_full)

        print(new_folder_name)
