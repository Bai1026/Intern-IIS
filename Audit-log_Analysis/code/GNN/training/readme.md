# This is the readme of the GNN training code of this project  
> Before the code explanation you should know:
- **Experiment 1**: do the **graph classification** with the 165 APs. And only contains the AP itself in each data input
- **Experiment 2**: do the **graph classification** with the 165 APs and 1 benign. And only contains the AP itself in each data input
- **Experiment 3**: do the **edge classification** with the the 165 APs and 1 benign. And the graph contains the neighbor benign nodes.  

- Example graph of experiment 1 and 2:
<img src="https://github.com/Bai1026/Intern-IIS/blob/main/Audit-log_Analysis/Figure/graph_self/T1003.002_7fa4ea18694f2552547b65e23952cabb.png" alt="error pic" width="550" height="550">

- Example graph of experiment 3:  
<img src="https://github.com/Bai1026/Intern-IIS/blob/main/Audit-log_Analysis/Figure/graph_with_benign/1003.001_0ef4cc7b-611c-4237-b20b-db36b6906554.png" alt="error pic" width="550" height="550">

> This part contains 2 folders:
- [Processing](https://github.com/Bai1026/Intern-IIS/tree/main/Audit-log_Analysis/code/GNN/processing)
- [Training](https://github.com/Bai1026/Intern-IIS/tree/main/Audit-log_Analysis/code/GNN/training)

<!-- ## Processing:  
- **change_graph_new.py**: change the original data to the input format of our training.
  - format of the result:  
    ```{"label": 9, "num_nodes": 3, "node_feat": [12, 20, 965], "edge_attr": [9, 7], "edge_index": [[0, 0], [1, 2]]}```
- **change_name_new.py**: change the label accroading to the mapping.txt
- **split.py**: split the training data with the ratio of ```8:1:1```
- **0_Graph_quick_look.ipynb**: make the benign graph with 4 specific versions.
  - 4 version of benign:  
    <img src="https://github.com/Bai1026/Intern-IIS/blob/main/Audit-log_Analysis/Figure/benign_version.png" alt="error pic" width="200" height="200">
    
- **add_embedding.py**: turn the node and edge features from original id to embedding of **Trans family**.
- **add_embedding_secure.ipynb**: turn the node and edge features from original id to embedding of **secureBERT family**.

- **merge.py**: for debugging.
- **check_num_of_files**: for debugging.
- **debug.py**: for debugging.
- **mapping.txt**: record the mapping of the true TTPs with their encoded label(int). -->


# This is the readme of the training part:
## Training:
> There are 4 types of training.  
> All of them have 11 versions of embedding for the node and edge id.  

> The **checkpoint** of the best performance would be stored at: ```../checkpoint_model_type/best_model_model_type_embedding_type.pt```  
> The **log message** contains the training message would be stored at:  
```../log_message/time_modeltype.log```  
> There would be **classification report** and **true-prediction comparison** files created and be stored at: ```../output_data_graphSAGE/exp_type/embedding_type/output_file```  

- **code_exp1-2**: use GAT or GCN model to do the experiment 1 and 2
- **code_exp3**:  use GAT or GCN model to do the experiment 3

- **graphSAGE_exp1-2**: use GraphSAGE model to do the experiment 1 and 2
- **graphSAGE_exp3**: use GraphSAGE model to do the experiment 3


## Prerequisites:
- Python 3.8 or higher
