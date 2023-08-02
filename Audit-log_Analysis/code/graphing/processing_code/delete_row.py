import os

input_file_path = '../data_new_entity/combined_file_new.txt'

with open(input_file_path, 'r') as input_file:
    output = []
    file_name, file_extension = os.path.splitext(input_file_path)
    output_file_path = f"{file_name}2{file_extension}"

    lines = input_file.readlines()[1:]  # 忽略第一行
    for line in lines:
        output.append(line)

    with open(output_file_path, 'w') as output_file:
        for line in output:
            output_file.write(line)
