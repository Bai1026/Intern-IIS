import os
import csv
import json
from tqdm import tqdm

input_folder = '../data/json_file'
output_folder = '../data/csv_file'

# go through all the files in the folder
for filename in tqdm(os.listdir(input_folder)):
    if filename.endswith('.json'):
        json_file_path = os.path.join(input_folder, filename)

        # read the json file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        rows = []
        for sentence in data['sentences']:
            text = sentence['text']
            mappings = sentence['mappings']
            attack_ids = [mapping['attack_id'] for mapping in mappings]
            for attack_id in attack_ids:
                rows.append([text, attack_id])

        csv_filename = f'{os.path.splitext(filename)[0]}.csv'
        output_file_path = os.path.join(output_folder, csv_filename)

        with open(output_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Text', 'Attack ID']) 
            writer.writerows(rows)  


# import os
# import json
# import pandas as pd

# input_folder = '../data/json_file'
# output_file_path = './output.xlsx'

# all_data = []

# for filename in os.listdir(input_folder):
#     if filename.endswith('.json'):
#         json_file_path = os.path.join(input_folder, filename)

#         with open(json_file_path, 'r') as json_file:
#             data = json.load(json_file)

#         for sentence in data['sentences']:
#             text = sentence['text']
#             mappings = sentence['mappings']
#             attack_ids = [mapping['attack_id'] for mapping in mappings]
#             for attack_id in attack_ids:
#                 all_data.append([text, attack_id])

# # 建立一個 DataFrame 來儲存所有的資料
# df = pd.DataFrame(all_data, columns=['Text', 'Attack ID'])

# # 將 DataFrame 寫入 Excel 檔案
# df.to_excel(output_file_path, index=False)

# print(f"All data has been written to '{output_file_path}'")

