import json

def convert_to_int64(data):
    # 轉換edge_index
    data["edge_index"] = [[int(src), int(dst)] for src, dst in data["edge_index"]]

    # 轉換node_feat
    data["node_feat"] = [[int(feat) for feat in node_feats] for node_feats in data["node_feat"]]

    # 轉換y
    data["y"] = [float(val) for val in data["y"]]

    return data

# 檔案路徑
file_paths = ["./data/train.jsonl", "./data/test.jsonl", "./data/valid.jsonl"]
for file_path in file_paths:
    with open(file_path, "r") as file:
        lines = file.readlines()
        processed_data = []
        for line in lines:
            data = json.loads(line)
            data = convert_to_int64(data)
            processed_data.append(data)
            # print(data)

        # 將處理完的data寫回檔案
        output_file_path = file_path.replace(".jsonl", "_processed.jsonl")
        with open(output_file_path, "w") as output_file:
            for data in processed_data:
                json.dump(data, output_file)
                output_file.write("\n")
