# 定義一個函式來讀取txt檔案並過濾資料
def filter_data(file_path):
    filtered_data = []
    count = 0
    with open(file_path, "r") as file:
        for line in file:
            source, destination, relation, entity, label = line.strip().split(' ')

            # 條件判斷：過濾掉label為'0'，以及開頭為'T1005'和'T1046'的relation
            # if label != '0' and not label.startswith('T1005') and not label.startswith('T1046'):
            # if label != 'benign' and not label.startswith('T1005') and not label.startswith('T1046'):
            if not label.startswith('T1005') and not label.startswith('T1046'):
                filtered_data.append(line.strip())
                count += 1
    return filtered_data

input_file_path = "./data_with_entity/labeled_with_entity.txt"  
output_file_path = "./data_with_entity/without_APs.txt"  

filtered_data = filter_data(input_file_path)

with open(output_file_path, "w") as output_file:
    for data in filtered_data:
        output_file.write(data + "\n")

print(f"總共過濾出 {len(filtered_data)} 筆符合條件的資料。")
