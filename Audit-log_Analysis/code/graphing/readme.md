# This is the readme of the graphing code of this project  
> These codes aim to **visualize the graph** we used in our GNN, including the node type, edge type → by shape  
> The data should be preprocessed through the previous code [here](https://github.com/Bai1026/Intern-IIS/tree/main/Audit-log_Analysis/code/GNN/processing)  
> This part contains 2 folders:
- [Graphing](https://github.com/Bai1026/Intern-IIS/tree/main/Audit-log_Analysis/code/graphing/graphing_code)
- [Processing](https://github.com/Bai1026/Intern-IIS/tree/main/Audit-log_Analysis/code/graphing/processing_code)

## Processing:  
- **add_benign.py**: add the string "benign" at the last of each row like other APs' format.
- **add_entity.py**: add the node's entity based on the mapping file.
- **label_filter.py**: filter out the data with the specific label like "benign", "T1005.xxx" and "T1046.xxx".
- **merge.py**: merge the data of the original data with the prediction based on the sigma rule to do the comparision.

- **show.py**: for debugging
- **delete_row.py**: for debugging
- **delete.py**: for debugging

## Graphing:
- **big_graph.py**: the graph contains all APs and generate in a single png file.  

- **graph_self.py**: create the graph of all the APs themselves, and output them as the png in a single folder.
- **graph_others.py**: create the graph of all the APs with the other neighbor nodes(1 hop), and output them as the png in a single folder.
- **graph_benign.py**: create the graph of all the APs with the other neighbor AP nodes and neighbor benign nodes(1 hop), and output them as the png in a single folder.

- **show_self.ipynb**: do the same thing as the graph_self except for this script shows the figures on the webpage and you can scroll.
- **show_others.ipynb**: do the same thing as the graph_others except for this script shows the figures on the webpage and you can scroll.
- **show_benign.ipynb**: do the same thing as the graph_benign except for this script shows the figures on the webpage and you can scroll.

- **subplot.ipynb**: let the graph_self's output be presented in 3 columns and 55 rows
- **subplot_only_benign.ipynb**: let the graph_benign's output be presented in 3 columns and 55 rows (we do not consider neighbor AP nodes here)

- **graph_sigma.py**: create the graph of the comparison of the prediction of the sigma rule and the true data, and we only consider APs themselves here. If the label is matched, the node would be red. Else if the label is not matched, the node would be translucent.

## Prerequisites:
- Python 3.8 or higher
