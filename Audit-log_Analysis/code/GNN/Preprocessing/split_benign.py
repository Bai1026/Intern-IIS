import os
from tqdm import tqdm
from collections import deque

# 从文件中读取数据并生成图
def generate_graphs(input_filename):
    data = []
    with open(input_filename, 'r') as file:
        for line in file:
            source, destination, relation = map(int, line.strip().split())
            data.append((source, destination, relation))
    return data

# 广度优先搜索生成图
def bfs(source, graph):
    visited = set()
    queue = deque([source])
    current_graph = []
    
    while queue and len(current_graph) < 32:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            current_graph.append(node)
            for _, destination, _ in graph:
                if destination == node and destination not in visited:
                    queue.append(destination)
    
    return current_graph

# 主函数
def main(input_filename, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    data = generate_graphs(input_filename)
    graph_id = 0
    visited_nodes = set()
    
    for source, _, _ in tqdm(data):
        if source not in visited_nodes:
            current_graph = bfs(source, data)
            visited_nodes.update(current_graph)
            
            output_filename = os.path.join(output_folder, f'{graph_id}.txt')
            with open(output_filename, 'w') as output_file:
                for node in current_graph:
                    output_file.write(str(node) + '\n')
            
            graph_id += 1

if __name__ == '__main__':
    input_filename = '../data_new/source_data/4_extended_APG_bai/benign.txt'  # 你的输入文件名
    output_folder = '../data_new/source_data/4_extended_APG_bai/benign'     # 存储图文件的文件夹名
    main(input_filename, output_folder)
