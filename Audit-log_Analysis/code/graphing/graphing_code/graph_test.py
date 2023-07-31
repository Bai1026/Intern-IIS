import os
from tqdm import tqdm
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

def read_data(file_path):
    edges = []
    with open(file_path, "r") as file:
        next(file) # skip the header
        for line in file:
            source, src_entity, destination, dest_entity, relation, label = line.strip().split(' ')
            # Since we only care about the main graph, we ignore benign, T1005 and T1046
            if label == 'benign' or label.startswith('T1005') or label.startswith('T1046'): continue
            edges.append((source, src_entity, destination, dest_entity, relation, label))
            
    return edges

def draw_graph(edges, file_name, target_label, title=None, figsize=(10, 8), dpi=100):
    G = nx.DiGraph()
    edge_labels = {}
    node_colors = {}
    edge_colors = {}
    node_shapes = {
        'process': 'o',    # Circle
        'registry': 'h',   # Hexagon
        'file': 's',       # Square
        'network': 'd'     # Diamond
    }

    for source, src_entity, destination, dest_entity, relation, label in edges:
        if label == target_label:
            # before adding the edge
            src_node_shape = node_shapes.get(src_entity, 'o')  # Use 'o' as the default shape
            dest_node_shape = node_shapes.get(dest_entity, 'o')  # Use 'o' as the default shape
            # print(src_entity, dest_entity) # correct

            # 檢查來源和目標節點是否存在，如果不存在就添加並設定形狀
            if source not in G.nodes:
                G.add_node(source)
                G.nodes[source]['shape'] = src_node_shape

            if destination not in G.nodes:
                G.add_node(destination)
                G.nodes[destination]['shape'] = dest_node_shape
            # print(G.nodes[destination]['shape'])


            edge = (source, destination)
            G.add_edge(source, destination)
            node_colors[source] = 'red'
            node_colors[destination] = 'red'
            edge_colors[(source, destination)] = 'red'

            if edge in edge_labels:
                edge_labels[edge] += ", " + relation
            else:
                edge_labels[edge] = relation

    
    pos = graphviz_layout(G, prog="dot")

    plt.figure(figsize=figsize)

    nx.draw_networkx_edges(G, pos)
    # nx.draw_networkx_nodes(G, pos, node_size=1500, node_color=[node_colors[node] for node in G.nodes()], node_shape='h')  # use 's' for square
    for node_type, shape in node_shapes.items():
        nx.draw_networkx_nodes(G, pos,
                            nodelist=[node for node, data in G.nodes(data=True) if data['shape'] == shape],
                            node_color='red',
                            node_size=1500,
                            node_shape=shape)

    nx.draw_networkx_labels(G, pos, font_size=8, font_color='black')

    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) # this code doesn't consider the multi-relation case
    edge_labels = {(source, destination): f"({len(relations.split(','))})" for (source, destination), relations in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if title:
        plt.text(0, 1, title, transform=plt.gca().transAxes, fontsize=12, fontweight='bold', verticalalignment='top')


    plt.axis('off')  # Turn off the axis frame
    plt.savefig(file_name + ".png", dpi=dpi)
    plt.show()
    plt.clf()

    print(f"Number of relations in the graph: {len(edges)}")


def is_valid_target_label(target_label):
    parts = target_label.split('_')
    return len(parts) >= 2 and len(parts[0]) > 0 and len(parts[1]) > 0

def draw_all_graphs(file_path):
    full_edges = read_data(file_path)

    unique_labels = set(edge[5] for edge in full_edges)
    label_edge_counts = {label: len([edge for edge in full_edges if edge[5] == label]) for label in unique_labels}
    sorted_labels = sorted(unique_labels, key=lambda x: label_edge_counts[x], reverse=True)

    os.makedirs("../graph_self/", exist_ok=True)

    for target_label in tqdm(sorted_labels):  # Use tqdm to display the progress
        if not is_valid_target_label(target_label):
            print(f"Invalid target_label: {target_label}") 
            continue

        target_edges = [edge for edge in full_edges if edge[5] == target_label]
        file_name = f"../graph_self/{target_label}"
        draw_graph(target_edges, file_name, target_label, title=target_label)
        print(f"{file_name}.png has been generated!")

file_path = "../data_new_entity/combined_file_with_entity.txt"

draw_all_graphs(file_path)
print("DONE!!")
