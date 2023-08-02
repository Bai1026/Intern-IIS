import os
import csv

# input_file_paths = ["../data_with_entity/without_APs.txt", 
#                     "../data_with_entity/without_APs_benign.txt", 
#                     "../data_with_entity/without_benign.txt"]  # 將輸入文件路徑列表進行替換

input_file_paths = ["../data_new_entity/combined_file.txt"]

for input_file_path in input_file_paths:
    # 获取文件名和扩展名
    file_name, file_extension = os.path.splitext(input_file_path)

    # 创建新的文件路径
    output_file_path = f"{file_name}_new{file_extension}"
    
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter=' ')
        writer = csv.writer(outfile, delimiter=' ')

        # Optional: Write header to the output file
        # writer.writerow(["src", "dest", "rel", "label"])

        for row in reader:
            # Skip rows that don't have the expected number of columns
            if len(row) != 5:
                continue

            src, dest, rel, _, label = row  # _ is a throwaway variable for the 'entity' column
            writer.writerow([src, dest, rel, label])
