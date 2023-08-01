import os
import numpy as np
import networkx as nx
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.patches as mpatches
from networkx.drawing.nx_agraph import graphviz_layout

def read_data(file_path):
    edges = []
    with open(file_path, "r") as file:
        next(file) # pass the 0th row (titles)

        for line in file:
            source, src_entity, destination, dest_entity, relation, label = line.strip().split(' ')
            # This is the without benign version
            if label == 'benign' or label.startswith('T1005') or label.startswith('T1046'): continue
            edges.append((source, src_entity, destination, dest_entity, relation, label))
            
    # edges is a list contains all the information (each set is stored in a tuple)
    return edges


def get_other_labels_edges(full_edges, related_nodes, target_label):
    other_labels_edges = []
    for edge in full_edges:
        source, src_entity, destination, dest_entity, relation, label = edge
        if label != target_label and (source in related_nodes or destination in related_nodes):
            other_labels_edges.append(edge)
    return other_labels_edges


def get_related_nodes(edges, target, is_label=True):
    related_nodes = set()

    for edge in edges:
        source, src_entity, destination, dest_entity, relation, label = edge
        if (is_label and label == target) or (not is_label and (source == target or destination == target)):
            related_nodes.add(source)
            related_nodes.add(destination)

    return related_nodes

def draw_graph(full_edges, target_edges, file_name, target_label, title=None, figsize=(10, 8), dpi=100):
    related_nodes = get_related_nodes(target_edges, title)  # only consider edges with target_label
    other_labels_edges = get_other_labels_edges(full_edges, related_nodes, title)

    # Separate edges into main graph and others
    main_edges = [edge for edge in target_edges if edge[-1] == target_label]
    other_edges = [edge for edge in target_edges if edge[-1] != target_label] + other_labels_edges

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

    # Extract unique labels (e.g., 'T1115_707' from 'T1115_70795de7cbb842edb029b3378c27c008')
    unique_labels = list(set([label.split('_')[0] + '_' + label.split('_')[1][:3] for _, _, _, _, _, label in other_edges]))  

    # Convert the target_label to same format as other labels
    target_label_modified = target_label.split('_')[0] + '_' + target_label.split('_')[1][:3]

    # Create a color map with unique colors for each label
    colors = cm.rainbow(np.linspace(0, 1, len(unique_labels)+1))
    red_color = np.array([1, 0, 0, 1])  # Red color
    color_map = {label: color for label, color in zip(unique_labels, colors) if not np.array_equal(color, red_color)}
    color_map[target_label_modified] = red_color  # Assign red color to the target label separately
    # color_map['benign'] = 'skyblue'  # Assign black color to the benign label
    print(color_map)

    # Add other edges
    for source, src_entity, destination, dest_entity, relation, label in other_edges:
        if label == '0': continue


        # before adding the edge
        src_node_shape = node_shapes.get(src_entity, 'o')  # Use 'o' as the default shape
        dest_node_shape = node_shapes.get(dest_entity, 'o')  # Use 'o' as the default shape
        print(src_entity, dest_entity) # correct

        # 檢查來源和目標節點是否存在，如果不存在就添加並設定形狀
        if source not in G.nodes:
            G.add_node(source)
            G.nodes[source]['shape'] = src_node_shape

        if destination not in G.nodes:
            G.add_node(destination)
            G.nodes[destination]['shape'] = dest_node_shape
        print(G.nodes[destination]['shape'])
        

        edge = (source, destination)
        if label != '0':
            label_prefix = label.split('_')[0]  # Get the first element after splitting by '_'
            label_prefix_extended = label_prefix + "_" + label.split('_')[1][:3]  # Add "_" and the first three characters after the second '_' to the label_prefix
        else:
            label_prefix_extended = 'benign'

        if edge in G.edges():
            edge_labels[edge] += ", " + relation
        else:
            G.add_edge(source, destination)

            # Check if the edge is a part of the target edges (main graph)
            if label == target_label:
                node_colors[source] = 'red'
                node_colors[destination] = 'red'
                edge_colors[edge] = 'red'
            else:
                node_colors[source] = color_map.get(label_prefix_extended, 'gray')  # Set gray as the default color
                node_colors[destination] = color_map.get(label_prefix_extended, 'gray')  # Set gray as the default color
                edge_colors[edge] = color_map.get(label_prefix_extended, 'black')

            edge_labels[edge] = relation

    # Add main graph edges
    for source, src_entity, destination, dest_entity, relation, label in main_edges:
        if label == 'benign': continue

        # before adding the edge
        src_node_shape = node_shapes.get(src_entity, 'o')  # Use 'o' as the default shape
        dest_node_shape = node_shapes.get(dest_entity, 'o')  # Use 'o' as the default shape
        print(src_entity, dest_entity) # correct

        # 檢查來源和目標節點是否存在，如果不存在就添加並設定形狀
        if source not in G.nodes:
            G.add_node(source)
            G.nodes[source]['shape'] = src_node_shape

        if destination not in G.nodes:
            G.add_node(destination)
            G.nodes[destination]['shape'] = dest_node_shape
        print(G.nodes[destination]['shape'])


        edge = (source, destination)
        G.add_edge(source, destination)
        node_colors[source] = 'red'
        node_colors[destination] = 'red'
        edge_colors[edge] = 'red'

        if edge in edge_labels:
            edge_labels[edge] += ", " + relation
        else:
            edge_labels[edge] = relation

    pos = graphviz_layout(G, prog="dot")
    pos = {node: (x, y-0.1) for node, (x, y) in pos.items()}

    plt.figure(figsize=figsize)

    # Draw nodes with custom label styles
    node_labels = {node: rf"$\bf{{{node}}}$" for node in G.nodes()}

    # nodelist=[node for node, data in G.nodes(data=True) if data['shape'] == shape]
    # colorlist = [node_colors.get(node, 'g') for node in nodelist]

    # nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color=[edge_colors[edge] for edge in G.edges()])

    # nx.draw(G, pos, with_labels=False, node_size=1500, font_size=8, node_color=[node_colors[node] for node in G.nodes()], edge_color=[edge_colors[edge] for edge in G.edges()], arrowsize=10, font_color='black')
    for shape in node_shapes.values():
        nodelist=[node for node, data in G.nodes(data=True) if data['shape'] == shape]
        colorlist = [node_colors.get(node, 'g') for node in nodelist]

        nx.draw_networkx_nodes(G, pos,
            nodelist=nodelist,
            node_color=colorlist,
            node_size=1500,
            node_shape=shape)


        
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, font_weight='bold', font_color='black')
    # Draw edges with custom edge labels
    edge_labels = {(source, destination): f"({len(relations.split(','))})" for (source, destination), relations in edge_labels.items()}
    # edge_color = [edge_colors[edge] if edge in edge_colors else 'black' for edge in G.edges()]
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if title:
        plt.text(0.05, 0.95, title, transform=plt.gca().transAxes, fontsize=12, fontweight='bold', verticalalignment='top')

    # for labeling all the label with the corresponding color
    patches = [mpatches.Patch(color=color, label=label) for label, color in color_map.items()]
    plt.legend(handles=patches)

    plt.savefig(file_name + ".png", dpi=dpi)
    plt.clf()


def get_related_nodes(edges, target_label):
    related_nodes = set()

    for edge in edges:
        if edge[5] == target_label:
            related_nodes.add(edge[0])
            related_nodes.add(edge[2]) # originally [1]

    return related_nodes


def get_other_labels_edges(full_edges, related_nodes, target_label):
    other_labels_edges = []
    for edge in full_edges:
        source, src_entity, destination, dest_entity, relation, label = edge
        if label != target_label and (source in related_nodes or destination in related_nodes):
            other_labels_edges.append(edge)
    return other_labels_edges


def is_valid_target_label(target_label):
    parts = target_label.split('_')
    return len(parts) >= 2 and len(parts[0]) > 0 and len(parts[1]) > 0

def draw_all_graphs(file_path):
    full_edges = read_data(file_path) 

    unique_labels = set(edge[5] for edge in full_edges)

    os.makedirs("../graph_others/", exist_ok=True)
    
    # every loop has it's own target label(unique)
    for target_label in unique_labels:
        if not is_valid_target_label(target_label):

            # Here we meet a label: "label" WTF -> solve this in the future
            print(f"Invalid target_label: {target_label}") 
            continue

        target_edges = [edge for edge in full_edges if edge[5] == target_label]

        file_name = f"../graph_others/{target_label}"
        draw_graph(full_edges, target_edges, file_name, target_label, title=target_label)
        print(f"{file_name}.png has been generated!")

file_path = "../data_with_entity/test.txt"

draw_all_graphs(file_path)
print("DONE!!")