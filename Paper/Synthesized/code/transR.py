import os
import traceback
import openke

from openke.config import Trainer, Tester
from openke.module.model import TransE, TransR
from openke.module.loss import MarginLoss
from openke.module.strategy import NegativeSampling
from openke.data import TrainDataLoader, TestDataLoader

os.environ['CUDA_VISIBLE_DEVICES'] = "3"
CPU_COUNT = os.cpu_count()

# if file_path is wrong -> segmentation fault
INPUT_PATH = '../data/3_openKE/'
OUTPUT_EMBEDDING_PATH = '../data/4_embedding'
OUTPUT_MODEL_PATH = '../data/4_embedding/model'
MODEL_NAME = 'transR'
DIM = 50 #可改：50, 100, 150
EMBEDDING_NAME = f'{MODEL_NAME}_{DIM}.vec.json'

# dataloader for training
print(f'Preparing train_dataloader...')
train_dataloader = TrainDataLoader(
	in_path = INPUT_PATH, 
	nbatches = 500,
	threads = CPU_COUNT, 
	sampling_mode = "normal", 
	bern_flag = 1, 
	filter_flag = 1, 
	neg_ent = 25,
	neg_rel = 0)

# define the model
print('Defining the model...')

transe = TransE(
	ent_tot = train_dataloader.get_ent_tot(),
	rel_tot = train_dataloader.get_rel_tot(),
	dim = DIM, 
	p_norm = 1, 
	norm_flag = True)

model_e = NegativeSampling(
	model = transe, 
	loss = MarginLoss(margin = 5.0),
	batch_size = train_dataloader.get_batch_size())

transr = TransR(
	ent_tot = train_dataloader.get_ent_tot(),
	rel_tot = train_dataloader.get_rel_tot(),
	dim_e = DIM,
	dim_r = DIM,
	p_norm = 1, 
	norm_flag = True,
    rand_init = False)

model_r = NegativeSampling(
	model = transr, 
	loss = MarginLoss(margin = 5.0),
	batch_size = train_dataloader.get_batch_size())

#pretrain transe
trainer = Trainer(model = model_e, data_loader = train_dataloader, train_times = 500, alpha = 0.5, use_gpu = True)
trainer.run()
parameters = transe.get_parameters()
transe.save_parameters(f"{OUTPUT_EMBEDDING_PATH}/transE_{DIM}.vec.json")

# transe.load_checkpoint(f'./data/3_openKE_model/v5/benign_and_expand_atk/transE_100.ckpt')
# parameters = transe.get_parameters()

# train transr
transr.set_parameters(parameters)
trainer = Trainer(model = model_r, data_loader = train_dataloader, train_times = 300, alpha = 1.0, use_gpu = True)
trainer.run()
transr.save_checkpoint(f'{OUTPUT_MODEL_PATH}/{MODEL_NAME}_{DIM}.ckpt')
print('Finish training the model')

# save the embeddings
print('Saving embedding...')
transr.save_parameters(f"{OUTPUT_EMBEDDING_PATH}/{EMBEDDING_NAME}")