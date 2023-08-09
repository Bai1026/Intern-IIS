import os
from tqdm import tqdm
from datasets import load_dataset
from sklearn.metrics import accuracy_score
# from torch import torch.optim.AdamW
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup
from transformers import Trainer, TrainingArguments, TrainerCallback, EvalPrediction, GraphormerForGraphClassification
from transformers.models.graphormer.collating_graphormer import preprocess_item, GraphormerDataCollator


dataset = load_dataset("OGB/ogbg-molhiv")
dataset_processed = dataset.map(preprocess_item, batched=False)

train_ds = dataset_processed['train']
val_ds = dataset_processed['validation']

model_checkpoint = "clefourrier/graphormer-base-pcqm4mv2" # pre-trained model from which to fine-tune

model = GraphormerForGraphClassification.from_pretrained(
    model_checkpoint, 
    num_classes=2,
    ignore_mismatched_sizes = True, # provide this in case you're planning to fine-tune an already fine-tuned checkpoint
)

training_args = TrainingArguments(
    "graph-classification",
    logging_dir="graph-classification",
    
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,

    auto_find_batch_size=True, # batch size can be changed automatically to prevent OOMs
    gradient_accumulation_steps=10,
    dataloader_num_workers=4, 

    num_train_epochs=20,

    evaluation_strategy="epoch",
    logging_strategy="epoch",
    push_to_hub=False,

    disable_tqdm=False,  # show the tqdm bar

)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    # eval_dataset=val_ds,
    data_collator=GraphormerDataCollator()
)


train_results = trainer.train()
# rest is optional but nice to have
trainer.save_model()
trainer.log_metrics("train", train_results.metrics)
trainer.save_metrics("train", train_results.metrics)
trainer.save_state()
