# This is the readme of the code that would be used in this project

> Structure of the file:

├── GNN: training code here
│    ├── *readme.md*
│    ├── checkpoint_graphSAGE
│    ├── checkpoint_graphSAGE_exp3
│    ├── graphSAGE_exp1-2: **training code** here
│    ├── graphSAGE_exp3: **training code** here
│    ├── log_message
│    ├── output_data_GraphSAGE
│    └── Old_models
│
└── data_processing
    ├── merge_raw_data.py: need to run this to get the format of: **[src, dest, rel, label]**
    ├── data_euni: raw data **from euni** stored here
    ├── dgl: all the datas first **preprocessing** here
    │   ├── *readme.md*
    │   ├── code_new
    │   ├── data_new
    │   └── old_version
    │
    └── graphing: specific for visualization
        ├── *readme.md*
        ├── benign
        ├── benign_with_entity
        ├── data
        ├── data_new_entity
        ├── data_with_entity
        ├── graphing_code: **graphing** here
        ├── graphs
        ├── out_benign
        └── processing_code: processing here for graph

- If you wanna have the graph in the essay:
    1. run the code "./data_processing/merge_raw_data.py" -> get the format contains the label
    2. run the code "./data_processing/graphing/processing_code/add_entity.py" -> get the data with node entity
    3. run the code you want in "./data_processing/graphing/graphing_code"

- If you wanna train the GNN model:
    1. run the code "./data_processing/merge_raw_data.py" -> get the format contains the label
    2. run the code in "./data_processing/dgl/code_new/" -> depends on what format u want
    3. run the code in "./GNN/graphSAGE_experiment_type/GraphSAGE_embedding_type.ipynb"
