import jsonlines

def find_row_without_node_feat(filename):
    target_key = "node_feat"

    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            data = jsonlines.Reader([line]).read()
            if isinstance(data, list) and len(data) > 0:
                item = data[0]
                if target_key not in item:
                    print(f"在第 {line_number} 行沒有 {target_key} 的資料。整列資料：{line}")

filename = '../data_new/training_data/valid.jsonl'
find_row_without_node_feat(filename)
print('hi')
