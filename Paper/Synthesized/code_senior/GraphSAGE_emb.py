import os
import json
import pickle
import random
import logging
import numpy as np
import pandas as pd
from glob import glob
from tqdm.notebook import tqdm
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report

import dgl
import dgl.nn as dglnn
from dgl.nn import GraphConv, GATConv, SAGEConv

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import AdamW, lr_scheduler
from torch.utils.data import Dataset, DataLoader
from transformers import get_linear_schedule_with_warmup

os.environ['CUDA_VISIBLE_DEVICES'] = "0"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S') 

import re

def build_dictionary(file_path):
    with open(file_path, 'r') as file:
        next(file)
        # 使用正则表达式去除行末的数字
        dictionary = {re.sub(r'\s\d+$', '', line.strip()): index for index, line in enumerate(file)}
    return dictionary

def get_value(event):
    global type2attr

    srcUUID = event["srcNode"]["UUID"]
    srcType = event["srcNode"]["Type"]
    srcAttr = event["srcNode"][type2attr[srcType]]
    dstUUID = event["dstNode"]["UUID"] if event["dstNode"] != None else srcUUID
    dstType = event["dstNode"]["Type"] if event["dstNode"] != None else srcType
    dstAttr = event["dstNode"][type2attr[dstType]] if event["dstNode"] != None else srcAttr
    return srcUUID, srcAttr, dstUUID, dstAttr, event["relation"], event["label"]

    def make_dataset(dataset):
    global node_ent2idx, edge_ent2idx, node_ent2emb, edge_ent2emb

    data_list = []
    for p in tqdm(dataset):
        with open(p) as fp:
            events = json.load(fp)
            
        nodes = set()
        edges = []
        relations = []
        labels = []
        uuid2res = {}
        for e in events:
            srcUUID, srcAttr, dstUUID, dstAttr, rel, label = get_value(e)

            uuid2res[srcUUID], uuid2res[dstUUID] = srcAttr, dstAttr
            nodes.add(srcUUID)
            nodes.add(dstUUID)
            edges.append((srcUUID, dstUUID))
            relations.append(edge_ent2idx[rel])
            labels.append(label2index[label])
        nodes = list(nodes)  
        node_feat = [torch.tensor(node_ent2emb[node_ent2idx[uuid2res[uuid]]], dtype=torch.float32) for uuid in nodes]
        edge_attr = [torch.tensor(edge_ent2emb[idx], dtype=torch.float32) for idx in relations]

        src = [nodes.index(src_uuid) for src_uuid, dst_uuid in edges]
        dst = [nodes.index(dst_uuid) for src_uuid, dst_uuid in edges]
        edge_index = torch.tensor([src, dst], dtype=torch.long)

        
        data_list.append({
            "labels": labels,
            "num_nodes": len(nodes),
            "node_feat": node_feat,
            "edge_attr": edge_attr,
            "edge_index": edge_index
        })
    return data_list         

file_path = '../data/3_openKE_3/label2id.txt'  # 替換為您檔案的路徑
label2index = build_dictionary(file_path)

label2index

index2label = {v: k for k, v in label2index.items()}

index2label

file_path = '../data/3_openKE_3/relation2id.txt'
edge_ent2idx = build_dictionary(file_path)

edge_ent2idx

# node_ent2idx = build_dictionary('../data/3_openKE/entity2id.txt')

with open (f'../data/3_openKE_2/entity2id.pkl', 'rb') as fp:
    node_ent2idx = pickle.load(fp)

print(node_ent2idx['4379921687c9a557f14c36d23279d6d4b8304e34d2cc904f9c8b9efed7824778.bin'])
print(node_ent2idx['HKLM\\System\\CurrentControlSet\\Control\\SafeBoot\\Option'])
print(node_ent2idx['\x1f@028;0 2K5740 70 3@0=8FC A>B@C4=8:0<.exe'])

DIM = 256
embedding = "transE"
embedding = f'{embedding}_{DIM}'

# with open(f"../data/4_embedding/{embedding}.vec.json", "r") as f:
with open(f"../data/4_embedding_3/{embedding}.vec.json", "r") as f:
    tmp = json.load(f)

node_ent2emb = {idx:emb for idx, emb in tqdm(enumerate(tmp["ent_embeddings.weight"]))}
edge_ent2emb = {idx:emb for idx, emb in tqdm(enumerate(tmp["rel_embeddings.weight"]))}

type2attr = {
    "Process": "Cmdline", 
    "File": "Name", 
    "Registry": "Key", 
    "Network": "Dstaddress"
}

random.seed(42)
trainset, validset, testset = [], [], []
for ability in tqdm(os.listdir('../data/Raw_dataset/')):
    paths = glob(f'../data/Raw_dataset/{ability}/number_*/expanded_instance.json')
    # paths = glob(f'../data/Raw_dataset/{ability}/number_*/expanded_instance.json')
    random.shuffle(paths)
    trainset.extend(paths[:80])
    validset.extend(paths[80:90])
    testset.extend(paths[90:])
    # break
    
train_data = make_dataset(trainset)
valid_data = make_dataset(validset)
test_data = make_dataset(testset)


class GraphDataset(Dataset):
    def __init__(self, data_list, device):
        self.data_list = data_list
        self.device = device

    def __len__(self):
        return len(self.data_list)
    
    def __getitem__(self, idx):
        data = self.data_list[idx]
        return data

def collate(samples):
    data_list = samples
    batched_graphs = []
    for data in data_list:
        g = dgl.graph((data["edge_index"][0], data["edge_index"][1]), num_nodes=data["num_nodes"])

        g.ndata['feat'] = torch.stack(data["node_feat"])
        g.edata['feat'] = torch.stack(data["edge_attr"])
        # print(data["labels"])
        g.edata['label'] = torch.tensor(data["labels"])  

        batched_graphs.append(g)
    
    return dgl.batch(batched_graphs)


train_GraphDataset = GraphDataset(train_data, device)
valid_GraphDataset = GraphDataset(valid_data, device)
test_GraphDataset = GraphDataset(test_data, device)

batch_size = 32

train_dataloader = DataLoader(train_GraphDataset, batch_size, shuffle=True, collate_fn=collate)
valid_dataloader = DataLoader(valid_GraphDataset, batch_size, shuffle=True, collate_fn=collate)
test_dataloader = DataLoader(test_GraphDataset, batch_size, shuffle=False, collate_fn=collate)

class GraphSAGE(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim):
        super(GraphSAGE, self).__init__()
        self.layer1 = dglnn.SAGEConv(in_dim, hidden_dim, 'pool')
        self.layer2 = dglnn.SAGEConv(hidden_dim, out_dim, 'pool')
        self.dropout = nn.Dropout(0.25)

    def forward(self, g, inputs):
        h = self.layer1(g, inputs)
        h = torch.relu(h)
        h = self.dropout(h)
        h = self.layer2(g, h)
        return h
    
class MLPPredictor(nn.Module):
    def __init__(self, out_feats, out_classes, edge_embedding_dim):
        super().__init__()
        self.W = nn.Linear(out_feats*2 + edge_embedding_dim, out_classes)

    def apply_edges(self, edges, edge_feat):
        h_u = edges.src['h']
        h_v = edges.dst['h']
        h_e = edge_feat
        score = self.W(torch.cat([h_u, h_v, h_e], 1))
        return {'score': score}

    def forward(self, graph, h, edge_feat):
        with graph.local_scope():
            graph.ndata['h'] = h
            # graph.apply_edges(self.apply_edges)
            graph.apply_edges(lambda edges: self.apply_edges(edges, edge_feat))
            return graph.edata['score']
        
class Model(nn.Module):
    def __init__(self, in_features, hidden_features, out_features, num_classes, edge_embedding_dim):
        super().__init__()
        self.sage = GraphSAGE(in_features, hidden_features, out_features)
        self.pred = MLPPredictor(out_features, num_classes, edge_embedding_dim)
      
    def forward(self, g, node_feat, edge_feat, return_logits=False):
        h = self.sage(g, node_feat)
        logits = self.pred(g, h, edge_feat)
        
        return logits

def same_seeds(seed = 42):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)  
    np.random.seed(seed)  
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True

def model_fn(batched_g, model, criterion, device, which_type='train'):
    """Forward a batch through the model."""
    batched_g = batched_g.to(device)
    
    labels = batched_g.edata['label'].to(device)    
    # logits = model(batched_g, batched_g.ndata['feat'].float())
    logits = model(batched_g, batched_g.ndata['feat'].float(), batched_g.edata['feat'].float())
    loss = criterion(logits, labels)

    output = torch.softmax(logits, dim=1)
    preds = output.argmax(1)
    # print(preds)
    
    accuracy = torch.mean((preds == labels).float())
        
    return loss, accuracy, preds

same_seeds(42)
model = Model(in_features=len(node_ent2emb[0]), hidden_features=64, out_features=128, num_classes=len(label2index), edge_embedding_dim = len(edge_ent2emb[0]))
model = model.to(device)
optimizer = AdamW(model.parameters(), lr=5e-4)
scheduler = lr_scheduler.CosineAnnealingLR(optimizer, T_max=20, eta_min=0, last_epoch=- 1, verbose=False)
criterion = nn.CrossEntropyLoss()
model_save_path = "./model/GraphSAGE_transE_256"
best_model_path = ''

best_val_loss = float('inf')

if not os.path.isdir(model_save_path):
    os.makedirs(model_save_path)

epochs = 200
best_val_loss = float('inf')
best_val_acc = float('-inf')
best_model_path = ""
for epoch in tqdm(range(epochs)):
    model.train()
    total_loss = 0.0
    total_accuracy = 0.0    
    for data in tqdm(train_dataloader):
        loss, accuracy, _ = model_fn(data, model, criterion, device, which_type='train')        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        total_accuracy += accuracy.item()

    scheduler.step()
    
    avg_loss = total_loss / len(train_dataloader)
    avg_accuracy = total_accuracy / len(train_dataloader)
    logging.info(f'Epoch {epoch} | Train Loss: {avg_loss:.4f} | Train Accuracy: {avg_accuracy:.4f}')
    
    # Validation Part
    model.eval()
    total_accuracy = 0.0
    total_loss = 0.0
    with torch.no_grad():
        for data in tqdm(valid_dataloader):
            loss, accuracy, _ = model_fn(data, model, criterion, device, which_type='validation')
            total_accuracy += accuracy.item()
            total_loss += loss.item()

    avg_accuracy = total_accuracy / len(valid_dataloader)
    current_loss = total_loss / len(valid_dataloader)
    # if current_loss < best_val_loss and avg_accuracy > best_val_acc:
    if current_loss < best_val_loss:
        best_val_loss = current_loss
        best_val_acc = avg_accuracy
        best_model_path = f'{model_save_path}/epoch_{epoch}_loss_{current_loss:.4f}_acc_{avg_accuracy:.4f}'
        print("Best Model Found!! ", best_model_path)
        
    logging.info(f'Validation Loss: {current_loss:.4f} | Validation Accuracy: {avg_accuracy:.4f}\n')    
    torch.save(model.state_dict(), f'{model_save_path}/epoch_{epoch}_loss_{current_loss:.4f}_acc_{avg_accuracy:.4f}')


# load the pretrained model
model.load_state_dict(torch.load(best_model_path))

model.to(device)
model.eval()

total = 0
correct = 0
true_labels = []
predicted_labels = []
with torch.no_grad():
    for data in test_dataloader:
        loss, accuracy, predicted = model_fn(data, model, criterion, device, which_type='test')
        labels = data.edata['label'].to(device)
        
        true_labels.extend(labels.cpu().numpy())
        predicted_labels.extend(predicted.cpu().numpy())
                
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

logging.info(f'Test Accuracy: {100 * correct / total:.4f} %\n\n\n')

report_data = classification_report(true_labels, predicted_labels, output_dict=True)
report_df = pd.DataFrame(report_data).transpose()

output_path = "./result/GraphSAGE_emb256"
if not os.path.isdir(output_path):
    os.makedirs(output_path)
    
report_df.reset_index(inplace=True, names='label')

label_list = []
for idx, row in report_df.iterrows():
    if row["label"].isdigit():
        row["label"] = index2label[int(row["label"])]
    label_list.append(row["label"])
report_df["label"] = label_list

report_df.to_csv(f'{output_path}/result.csv', index=False)
print("report output at: ", f'{output_path}/result.csv')

report_df