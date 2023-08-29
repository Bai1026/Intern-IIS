import os

# 初始化
folder_path = "../data_new/source_data/4_extended_APG_bai"
folder_names = os.listdir(folder_path)
new_mapping = {}  # 用于存放新的映射关系
counter = 0  # 用于递增的计数器

for folder_name in folder_names:
    if "(" in folder_name:
        key_name = folder_name.split("(")[0]

        # 使用计数器的值作为新的文件夹名
        new_folder_name = str(counter)

        os.rename(os.path.join(folder_path, folder_name), os.path.join(folder_path, new_folder_name))
        print(f"Renamed {folder_name} to {new_folder_name}")

        # 保存映射关系
        new_mapping[key_name] = counter
        counter += 1

# 将新的映射关系写入文件
with open("new_mapping.txt", "w") as f:
    for key, value in new_mapping.items():
        f.write(f"{key}: {value}\n")
