# This is the readme of the GNN training code of this project  
> Before the code explanation you should know:
- **Experiment 1**: do the **graph classification** with the 165 APs. And only contains the AP itself in each data input
- **Experiment 2**: do the **graph classification** with the 165 APs and 1 benign. And only contains the AP itself in each data input
- **Experiment 3**: do the **edge classification** with the the 165 APs and 1 benign. And the graph contains the neighbor benign nodes.  

- Example graph of experiment 1 and 2:
<img src="https://github.com/Bai1026/Intern-IIS/blob/main/Audit-log_Analysis/Figure/graph_self/T1003.002_7fa4ea18694f2552547b65e23952cabb.png" alt="error pic" width="650" height="650">

- Example graph of experiment 3:  
<img src="https://github.com/Bai1026/Intern-IIS/blob/main/Audit-log_Analysis/Figure/graph_with_benign/1003.001_0ef4cc7b-611c-4237-b20b-db36b6906554.png" alt="error pic" width="650" height="650">

> This part contains 2 folders:
- [Processing](https://github.com/Bai1026/Intern-IIS/tree/main/Audit-log_Analysis/code/GNN/processing)
- [Training](https://github.com/Bai1026/Intern-IIS/tree/main/Audit-log_Analysis/code/GNN/training)

## Processing:  
- **add_benign.py**: add the string "benign" at the last of each row like other APs' format.
- **add_entity.py**: add the node's entity based on the mapping file.
- **label_filter.py**: filter out the data with the specific label like "benign", "T1005.xxx" and "T1046.xxx".
- **merge.py**: merge the data of the original data with the prediction based on the sigma rule to do the comparision.

- **show.py**: for debugging
- **delete_row.py**: for debugging
- **delete.py**: for debugging

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
