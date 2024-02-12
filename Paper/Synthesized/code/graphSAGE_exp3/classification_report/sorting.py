'''This is the python script to make the order of the labels all the same between RNN, MLP, GNN'''

import os
import pandas as pd

def sort_key(s):
    parts = s.split('_')
    num_parts = parts[0][1:].split('.')
    num_parts = [int(part) for part in num_parts]
    rest = parts[1] if len(parts) > 1 else ''
    return (*num_parts, rest)

xlsx_file = './filtered_mapped_true_predicted_labels-transR_50-graphSAGE-11.xlsx'  # 替换为你的文件路径
df = pd.read_excel(xlsx_file, engine='openpyxl')

df_sorted = df.sort_values(by='true_label', key=lambda col: col.map(sort_key))

dirname, filename = os.path.split(xlsx_file)
filename = 'sorted_' + filename
output_xlsx_file = os.path.join(dirname, filename)

df_sorted.to_excel(output_xlsx_file, index=False)

print(f'Sorted data has been written to {output_xlsx_file}')