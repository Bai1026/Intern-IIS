import json
from tqdm import tqdm

# Load data
data = []
with open("../data/remaining_data_5.jsonl", "r") as f:
    for line in f:
        item = json.loads(line.strip())
        if item["y"][0] == 0:
            data.append(item)

# Helper function to use DFS for finding connected components (subgraphs)
def dfs(node, visited, subgraph):
    visited.add(node)
    subgraph.append(node)

    # Check the connections of this node
    for item in data:
        src, _, dst = [feat[0] for feat in item["node_feat"]]
        if node == src and dst not in visited:
            dfs(dst, visited, subgraph)
        elif node == dst and src not in visited:
            dfs(src, visited, subgraph)

# Helper function to transform subgraphs
def transform_subgraphs(subgraphs):
    nodes = []
    edges = []
    edge_attrs = []
    
    for subgraph in tqdm(subgraphs):
        src, edge_attr, dst = [feat[0] for feat in subgraph["node_feat"]]

        if src not in nodes:
            nodes.append(src)
        if dst not in nodes:
            nodes.append(dst)

        source_idx = nodes.index(src)
        target_idx = nodes.index(dst)
        edges.append([source_idx, target_idx])
        edge_attrs.append(edge_attr)

    edges = list(zip(*edges))
    return {
        "label": subgraphs[0]["y"][0],
        "num_nodes": len(nodes),
        "node_feat": nodes,
        "edge_attr": edge_attrs,
        "edge_index": edges
    }

visited_nodes = set()
connected_subgraphs = []

for item in tqdm(data):
    src, _, dst = [feat[0] for feat in item["node_feat"]]
    if src not in visited_nodes:
        subgraph = []
        dfs(src, visited_nodes, subgraph)
        connected_subgraphs.append(subgraph)

# Take the first 50 subgraphs
first_50_subgraphs = []
for subgraph_nodes in tqdm(connected_subgraphs[:50]):
    subgraph = [item for item in data if item["node_feat"][0][0] in subgraph_nodes or item["node_feat"][2][0] in subgraph_nodes]
    first_50_subgraphs.append(transform_subgraphs(subgraph))

# Save the transformed subgraphs
output_file = "../data/output/transformed_subgraphs_label0_50-5.jsonl"
with open(output_file, "w") as f:
    for subgraph in first_50_subgraphs:
        f.write(json.dumps(subgraph) + "\n")



# import json
# from tqdm import tqdm

# class UnionFind:
#     def __init__(self):
#         self.parent = {}
#         self.rank = {}

#     def find(self, x):
#         if x not in self.parent:
#             self.parent[x] = x
#             self.rank[x] = 0
#         path = []
#         while self.parent[x] != x:
#             path.append(x)
#             x = self.parent[x]

#         # Flatten the path
#         for node in path:
#             self.parent[node] = x

#         return x

#     def union(self, x, y):
#         if x not in self.parent:
#             self.parent[x] = x
#             self.rank[x] = 0
#         if y not in self.parent:
#             self.parent[y] = y
#             self.rank[y] = 0
            
#         rootX = self.find(x)
#         rootY = self.find(y)
#         if rootX != rootY:
#             if self.rank[rootX] > self.rank[rootY]:
#                 self.parent[rootY] = rootX
#             else:
#                 self.parent[rootX] = rootY
#                 if self.rank[rootX] == self.rank[rootY]:
#                     self.rank[rootY] += 1



# # Load data
# data = []
# with open("../data/remaining_data_0.05.jsonl", "r") as f:
#     for line in f:
#         item = json.loads(line.strip())
#         if item["y"][0] == 0:
#             data.append(item)

# uf = UnionFind()

# for item in tqdm(data):
#     src, _, dst = [feat[0] for feat in item["node_feat"]]
#     uf.union(src, dst)

# # Group by parent (representative element of the set)
# groups = {}
# for node in tqdm(uf.parent.keys()):
#     root = uf.find(node)
#     if root not in groups:
#         groups[root] = []
#     groups[root].append(node)

# # Sort groups by size
# sorted_groups = sorted(groups.values(), key=len, reverse=False)

# # Transform data according to the groups
# result = []

# for group in tqdm(sorted_groups[:50]):
#     nodes = group
#     edges = []
#     edge_attrs = []
#     for item in data:
#         src, edge_attr, dst = [feat[0] for feat in item["node_feat"]]
#         if src in nodes and dst in nodes:
#             source_idx = nodes.index(src)
#             target_idx = nodes.index(dst)
#             edges.append([source_idx, target_idx])
#             edge_attrs.append(edge_attr)

#     edges = list(zip(*edges))
#     result.append({
#         "label": 0,
#         "num_nodes": len(nodes),
#         "node_feat": nodes,
#         "edge_attr": edge_attrs,
#         "edge_index": edges
#     })

# # Save the transformed subgraphs
# output_file = "../data/transformed_subgraphs_label0_50.jsonl"
# with open(output_file, "w") as f:
#     for subgraph in result:
#         f.write(json.dumps(subgraph) + "\n")
