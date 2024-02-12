import os
import traceback
from openke.config import Trainer, Tester
from openke.module.model import TransH
from openke.module.loss import MarginLoss
from openke.module.strategy import NegativeSampling
from openke.data import TrainDataLoader, TestDataLoader
os.environ['CUDA_VISIBLE_DEVICES'] = "3"

# if file_path is wrong -> segmentation fault
INPUT_PATH = '../data/3_openKE/'
OUTPUT_EMBEDDING_PATH = '../data/4_embedding'
OUTPUT_MODEL_PATH = '../data/4_embedding/model'
MODEL_NAME = 'transH'
DIM = 50 #可改：50, 100, 150
EMBEDDING_NAME = f'{MODEL_NAME}_{DIM}.vec.json'

# dataloader for training
print(f'Preparing train_dataloader...')
train_dataloader = TrainDataLoader(
	in_path = INPUT_PATH, 
	nbatches = 500,
	threads = os.cpu_count(), 
	sampling_mode = "normal", 
	bern_flag = 1, 
	filter_flag = 1, 
	neg_ent = 25,
	neg_rel = 0)

# define the model
print('Defining the model...')
transh = TransH(
	ent_tot = train_dataloader.get_ent_tot(),
	rel_tot = train_dataloader.get_rel_tot(),
	dim = DIM, 
	p_norm = 1, 
	norm_flag = True)

model_h = NegativeSampling(
	model = transh, 
	loss = MarginLoss(margin = 5.0),
	batch_size = train_dataloader.get_batch_size())

# train transh
trainer = Trainer(model = model_h, data_loader = train_dataloader, train_times = 500, alpha = 1.0, use_gpu = True)
trainer.run()
transh.save_checkpoint(f'{OUTPUT_MODEL_PATH}/{MODEL_NAME}_{DIM}.ckpt')
print('Finish training the model')


# save the embeddings
print('Saving embedding...')
transh.save_parameters(f"{OUTPUT_EMBEDDING_PATH}/{EMBEDDING_NAME}")