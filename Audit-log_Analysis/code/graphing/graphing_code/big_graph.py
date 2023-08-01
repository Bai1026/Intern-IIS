# import os
import matplotlib.cm as cm
import numpy as np
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

def draw_big_graph(edges, file_name, figsize=(120, 48), dpi=200):
    G = nx.DiGraph()
    edge_labels = {}
    edge_colors = {}
    unique_labels = list(set(edge[5] for edge in full_edges))
    colors = cm.rainbow(np.linspace(0, 1, len(unique_labels)))
    label_color_map = dict(zip(unique_labels, colors))  
    
    for source, src_entity, destination, dest_entity, relation, label in edges:
        edge = (source, destination)
        G.add_edge(source, destination)
        if edge in edge_labels:
            edge_labels[edge] += ", " + label
        else:
            edge_labels[edge] = label

        color = label_color_map[label]
        edge_colors[(source, destination)] = color 

    pos = graphviz_layout(G, prog="dot")
    plt.figure(figsize=figsize)
    nx.draw_networkx_edges(G, pos)
    # nx.draw_networkx_labels(G, pos, font_size=8, font_color='black')

    # edge_labels = {(source, destination): f"({len(relations.split(','))})" for (source, destination), relations in edge_labels.items()}
    # nx.draw_networkx_edge_labels(G, pos)
    # # Label is the num of the labels
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # # No label, only edge color which is depending on the AP
    nx.draw_networkx_edges(G, pos, edge_color=[edge_colors[edge] for edge in G.edges()])


    plt.axis('off')  # Turn off the axis frame
    plt.savefig(file_name + ".png", dpi=dpi)
    plt.clf()

file_path = "../data_new_entity/combined_file_with_entity.txt"
full_edges = read_data(file_path)

draw_big_graph(full_edges, "big_graph")

print("DONE!!")
