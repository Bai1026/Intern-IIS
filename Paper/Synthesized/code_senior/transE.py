import os

import openke
from openke.config import Trainer, Tester
from openke.module.model import TransE, TransR
from openke.module.loss import MarginLoss
from openke.module.strategy import NegativeSampling
from openke.data import TrainDataLoader, TestDataLoader


DIM = 150
MODEL_NAME = 'transE'
EMBEDDING_NAME = f'{MODEL_NAME}_{DIM}.vec.json'
OUTPUT_EMBEDDING_PATH = '../data/4_embedding'

os.environ['CUDA_VISIBLE_DEVICES'] = '0'


# dataloader for training
train_dataloader = TrainDataLoader(
    in_path = "../data/3_openKE/", 
    nbatches = 100,
    threads = 8, 
    sampling_mode = "normal", 
    bern_flag = 1, 
    filter_flag = 1, 
    neg_ent = 25,
    neg_rel = 0)

# dataloader for test
test_dataloader = TestDataLoader("../data/3_openKE/", "link")

# define the model
transe = TransE(
    ent_tot = train_dataloader.get_ent_tot(),
    rel_tot = train_dataloader.get_rel_tot(),
    dim = DIM, 
    p_norm = 1, 
    norm_flag = True)

# define the loss function
model = NegativeSampling(
    model = transe, 
    loss = MarginLoss(margin = 5.0),
    batch_size = train_dataloader.get_batch_size()
)

trainer = Trainer(model = model, data_loader = train_dataloader, train_times = 500, alpha = 1.0, use_gpu = True)
trainer.run()
transe.save_checkpoint('./checkpoint/transe.ckpt')

# save the embeddings
print('Saving embedding...')
transe.save_parameters(f"{OUTPUT_EMBEDDING_PATH}/{EMBEDDING_NAME}")