import os

# folder_paths = ["./with_benign", "./without_benign"]
folder_paths = ['4_extended_APG_with_benign']

count = sum(len(os.listdir(folder_path)) for folder_path in folder_paths)

print(f"There're {count} number of the folder")

# with open(file_path1, 'r') as file1:
#     for line in file1:

