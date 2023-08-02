import os

id_entity_dict = {}
with open('../data_new_entity/entity2id_objType.txt', 'r') as file:
    lines = file.readlines()
    for line in lines[1:]: # start from the 2nd row
        entity, id = line.strip().split() # Assumes that id and entity are separated by a space
        id_entity_dict[int(id)] = entity

# 讀取並處理原始txt file
# file_paths = ["without_APs_benign_new.txt", "without_benign_new.txt", "without_APs_new.txt"]
# file_paths = ['../data_new_entity/test.txt']
file_paths = ['../data_new_entity/combined_file_new.txt']

for input_file in file_paths:
    data = []
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]: # Skip header 
            src, dest, rel, label = line.strip().split(' ') # Assumes that src, dest, rel and label are separated by commas
            src = int(src)
            dest = int(dest)
            src_entity = id_entity_dict.get(src, 'Unknown')
            dest_entity = id_entity_dict.get(dest, 'Unknown')
            data.append([src, src_entity, dest, dest_entity, rel, label])

    file_name, file_extension = os.path.splitext(input_file)
    file_name = file_name.replace('file_new', 'file_with_entity')
    output_file_path = f"{file_name}{file_extension}"
    # output_file_path = f"{file_name}_out{file_extension}"

    # 寫入新的txt file
    with open(output_file_path, 'w') as file:
        file.write('src, src_entity, dest, dest_entity, rel, label\n') # Write header
        for line in data:
            file.write(' '.join(map(str, line)) + '\n') # Convert all elements to string and join them with commas

