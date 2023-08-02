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
            source, src_entity, destination, dest_entity, relation, label, sigma = line.strip().split(' ')
            # Since we only care about the main graph, we ignore benign, T1005 and T1046
            if label == 'benign' or label.startswith('T1005') or label.startswith('T1046'): continue
            edges.append((source, src_entity, destination, dest_entity, relation, label, sigma.split(',')))
    return edges


def draw_graph(edges, file_name, target_label, title=None, figsize=(10, 8), dpi=100):

    G = nx.DiGraph()
    edge_labels = {}
    node_colors = {}
    edge_colors = {}
    edge_styles = {}
    node_shapes = {
        'process': 'o',    # Circle
        'registry': 'h',   # Hexagon
        'file': 's',       # Square
        'network': 'd'     # Diamond
    }

    # initialize all the nodes
    node_colors = {node: 'none' for node in (edge[i] for edge in edges for i in [0, 2])}
    # node_colors = {node: 'red' for node in (edge[i] for edge in edges for i in [0, 2])}
    # initialize all the nodes as half-transparent red
    # node_colors = {node: (1, 0, 0, 0.25) for node in (edge[i] for edge in edges for i in [0, 2])}



    # for source, src_entity, destination, dest_entity, relation, label, sigma in edges:
    #     if label == target_label:
    #         edge = (source, destination)
    #         if label.split('_')[0] in sigma:  # Check if label is in sigma
    #             node_colors[edge] = 'red'
    #             edge_colors[edge] = 'red'
    #             edge_styles[edge] = 'solid'
    #         else:
    #             node_colors[edge] = 'none'
    #             edge_colors[edge] = 'black'
    #             edge_styles[edge] = 'dashed'
    for source, src_entity, destination, dest_entity, relation, label, sigma in edges:
        if label == target_label:
            edge = (source, destination)
            if label.split('_')[0] in sigma:  # Check if label is in sigma
                node_colors[source] = 'red'
                node_colors[destination] = 'red'
                edge_colors[edge] = 'red'
                edge_styles[edge] = 'solid'
            else:
                if node_colors[source] == 'red':
                    node_colors[destination] = (1, 0, 0, 0.25)  # Half-transparent red
                else:
                    node_colors[source] = (1, 0, 0, 0.25)  # Half-transparent red
                    node_colors[destination] = (1, 0, 0, 0.25)  # Half-transparent red

                edge_colors[edge] = 'black'
                edge_styles[edge] = 'dashed'

    # for source, src_entity, destination, dest_entity, relation, label, sigma in edges:
    #     edge = (source, destination)
    #     if label == target_label and label.split('_')[0] in sigma:  # Check if label is in sigma
    #         node_colors[source] = 'red'
    #         node_colors[destination] = 'red'
    #         edge_colors[edge] = 'red'
    #         edge_styles[edge] = 'solid'
    #     else:
    #         edge_colors[edge] = 'black'
    #         edge_styles[edge] = 'dashed'

            src_node_shape = node_shapes.get(src_entity, 'o')  # Use 'o' as the default shape
            dest_node_shape = node_shapes.get(dest_entity, 'o')  # Use 'o' as the default shape

            if source not in G.nodes:
                G.add_node(source)
                G.nodes[source]['shape'] = src_node_shape
            if destination not in G.nodes:
                G.add_node(destination)
                G.nodes[destination]['shape'] = dest_node_shape
            
            G.add_edge(source, destination)

            if edge in edge_labels:
                edge_labels[edge] += ", " + relation
            else:
                edge_labels[edge] = relation

    pos = graphviz_layout(G, prog="dot")

    plt.figure(figsize=figsize)
    
    nx.draw_networkx_edges(G, pos, edge_color=[edge_colors.get(edge, 'black') for edge in G.edges()], style=[edge_styles[edge] for edge in G.edges()])


    for node_type, shape in node_shapes.items():

        nodelist=[node for node, data in G.nodes(data=True) if data['shape'] == shape]
        nx.draw_networkx_nodes(G, pos,
                       nodelist=nodelist,
                       node_color=[node_colors.get(node, 'red') for node in nodelist],
                       node_size=1500,
                       node_shape=shape)
    print(node_colors)

    nx.draw_networkx_labels(G, pos, font_size=8, font_color='black')

    edge_labels = {(source, destination): f"({len(relations.split(','))})" for (source, destination), relations in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)


    if title:
        plt.text(0, 1, title, transform=plt.gca().transAxes, fontsize=12, fontweight='bold', verticalalignment='top')

    plt.axis('off')  # Turn off the axis frame
    plt.savefig(file_name + ".png", dpi=dpi)
    plt.clf()


def is_valid_target_label(target_label):
    parts = target_label.split('_')
    return len(parts) >= 2 and len(parts[0]) > 0 and len(parts[1]) > 0

def draw_all_graphs(file_path):
    full_edges = read_data(file_path)

    unique_labels = set(edge[5] for edge in full_edges)

    os.makedirs("../graphs/graph_sigma2/", exist_ok=True)
    # os.makedirs("./graph_sigma_test2/", exist_ok=True)
    # count = 0

    for target_label in tqdm(unique_labels):  # Use tqdm to display the progress
        # count += 1
        # if count == 20: break

        if not is_valid_target_label(target_label):
            print(f"Invalid target_label: {target_label}") 
            continue

        target_edges = [edge for edge in full_edges if edge[5] == target_label]
        file_name = f"../graphs/graph_sigma2/{target_label}"
        draw_graph(target_edges, file_name, target_label, title=target_label)
        print(f"{file_name}.png has been generated!")

file_path = "../data_new_entity/data_with_sigma.txt"

draw_all_graphs(file_path)
print("DONE!!")
