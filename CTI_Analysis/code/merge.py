import os
import pandas as pd
from tqdm import tqdm

INPUT_FOLDER = '/Volumes/K16/CTI_report/all_csv'
# INPUT_FOLDER = '/Volumes/K16/CTI_report/test'
OUTPUT_FILE = '../data/output.xlsx'

# get the list of the files' names in the input folder
csv_files = [file for file in os.listdir(INPUT_FOLDER) if file.endswith('.csv')]
# print(csv_files)

# for unique TTP, use set()
unique_attack_ids = set()

# get all the possible Attack ID
for csv_file in tqdm(csv_files):
    # use os to join the file path
    file_path = os.path.join(INPUT_FOLDER, csv_file)

    try:
        df = pd.read_csv(file_path, sep=',', encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(file_path, sep=',', encoding='utf-16')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, sep=',', encoding='latin-1')

    # update the unique lables; .unique would return the unique values in the set()
    unique_attack_ids.update(df['Attack ID'].unique())

unique_attack_ids = list(unique_attack_ids)


# 初始化数据框
result_df = pd.DataFrame(columns=['file_name'] + unique_attack_ids)

for csv_file in tqdm(csv_files):
    file_path = os.path.join(INPUT_FOLDER, csv_file)

    df = pd.read_csv(file_path, sep=',', quotechar='"', encoding='utf-8')
    
    # split the file name and the .csv
    file_name = os.path.splitext(csv_file)[0]

    # 這行代碼首先對DataFrame中的'Attack ID'列進行計數，計算每個不同的攻擊ID在該CSV文件中出現的次數。函數value_counts()返回一個包含不同攻擊ID及其出現次數的系列，
    # 然後通過格式對應.to_dict()系列轉換為字典，其中鍵是攻擊ID，值是對應的出現次數。這樣就得到了一個字典attack_id_counts，用於表示每個攻擊ID的出現次數。
    attack_id_counts = df['Attack ID'].value_counts().to_dict()
    
    # 這行代碼創建了一個數據行，包含文件名和每個不同攻擊ID的出現次數。file_name是當前處理的CSV文件的文件名，是數據行的第一個元素。
    # 然後，通過遍歷unique_attack_ids列表中的每個不同的攻擊ID，使用attack_id_counts.get(attack_id, 0)來獲取該攻擊ID在attack_id_counts字典中的出現次數。
    # 如果該攻擊ID不存在於字典中（即在當前CSV文件中未出現），則返回0。這樣，獲取的列表就包含了文件名和每個攻擊 ID 的出現次數。最終此列表將被添加到結果數據框，用於構建最終的 Excel 表格。
    data_row = [file_name] + [attack_id_counts.get(attack_id, 0) for attack_id in unique_attack_ids]

    # insert at len(result_df) would be a new line
    result_df.loc[len(result_df)] = data_row

result_df.to_excel(OUTPUT_FILE, index=False)
