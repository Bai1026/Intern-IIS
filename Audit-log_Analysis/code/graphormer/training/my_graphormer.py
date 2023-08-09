import os
from tqdm import tqdm
from datasets import load_dataset
from sklearn.metrics import accuracy_score
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup
from transformers import Trainer, TrainingArguments, TrainerCallback, EvalPrediction, GraphormerForGraphClassification
from transformers.models.graphormer.collating_graphormer import preprocess_item, GraphormerDataCollator


class PrintInfoCallback(TrainerCallback):
    def on_log(self, args, state, control, model, logs=None, **kwargs):
        print(f"Epoch: {state.epoch}, Step: {state.global_step}, Loss: {logs['loss']}")


def compute_accuracy(p: EvalPrediction):
    preds = p.predictions.argmax(-1)
    return {"accuracy": accuracy_score(p.label_ids, preds)}


# CUDA_VISIBLE_DEVICES = "0,1,2"
# os.environ['CUDA_LAUNCH_BLOCKING'] = "1"


dataset = load_dataset("VincentPai/encoded-MITRE-small")
dataset = dataset.shuffle(seed = 87)
dataset_processed = dataset.map(preprocess_item, batched=False)

# split up training into training + validation
train_ds = dataset_processed['train']
val_ds = dataset_processed['validation']


model_checkpoint = "clefourrier/graphormer-base-pcqm4mv2" # pre-trained model from which to fine-tune

model = GraphormerForGraphClassification.from_pretrained(
    model_checkpoint, 
    # We have 167 attack patterns and 1 benign
    num_classes=168, 
    # provide this in case you're planning to fine-tune
    # an already fine-tuned checkpoint
    ignore_mismatched_sizes = True, 
)


training_args = TrainingArguments(
    "graph-classification",
    logging_dir="graph-classification",
    
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,

    # batch size changed automatically to prevent OOMs
    auto_find_batch_size=True, 
    gradient_accumulation_steps=10,
    dataloader_num_workers=4, 
    num_train_epochs=5,

    evaluation_strategy="epoch",
    logging_strategy="epoch",
    push_to_hub=False,
    disable_tqdm=False,
)

# 你需要定义一些参数
num_training_steps = len(train_ds) * training_args.num_train_epochs // training_args.per_device_train_batch_size // training_args.gradient_accumulation_steps
num_warmup_steps = num_training_steps // 10

optimizer = AdamW(model.parameters(), lr=5e-5)
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps, num_training_steps)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    data_collator=GraphormerDataCollator(),
    callbacks=[PrintInfoCallback()],
    compute_metrics=compute_accuracy,
    optimizers=(optimizer, scheduler),
)

'''
optimizers (Tuple[torch.optim.Optimizer, torch.optim.lr_scheduler.LambdaLR], optional) 
A tuple containing the optimizer and the scheduler to use.
Will default to an instance of AdamW on your model and a scheduler given by get_linear_schedule_with_warmup() controlled by args.
'''

train_results = trainer.train()

# rest is optional but nice to have
trainer.save_model()
trainer.log_metrics("train", train_results.metrics)
trainer.save_metrics("train", train_results.metrics)
trainer.save_state()
