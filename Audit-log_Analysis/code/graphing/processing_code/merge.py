# 讀取第一個檔案的內容
with open('../data_euni/train2id.txt', 'r') as file1:
    lines_file1 = file1.readlines()

# 讀取第二個檔案的內容
with open('../data_euni/train2id_label.txt', 'r') as file2:
    lines_file2 = file2.readlines()

# 結合兩個檔案並加上標題
combined_data = []
combined_data.append("src, dest, rel, entity, label")

for i in range(1,len(lines_file1)):
    src, dest, rel = map(int, lines_file1[i].strip().split())
    entity, label = lines_file2[i].strip().split()
    combined_data.append(f"{src} {dest} {rel} {entity} {label}")

# 將結合後的資料寫入新的檔案中
with open('combined_file.txt', 'w') as output_file:
    for line in combined_data:
        output_file.write(line + '\n')

print("檔案已結合並保存為 'combined_file.txt'")
