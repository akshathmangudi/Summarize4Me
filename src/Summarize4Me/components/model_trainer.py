import os
from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset, load_from_disk
from Summarize4Me.entity import ModelTrainerConfig
import torch


# The main model training of the program, which has all the hyperparameters.
class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        """
        This method will train the model from the data_ingestion as input and generate a model and a tokenizer
        under artifacts/model_trainer.
        """
        device = "gpu" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.pretrained_model)
        pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.pretrained_model).to(device)
        seq2seq_collator = DataCollatorForSeq2Seq(tokenizer, model=pegasus)

        dataset_samsum = load_from_disk(self.config.data_path)

        trainer_args = TrainingArguments(
            output_dir=self.config.root_dir,
            num_train_epochs=1,
            warmup_steps=50,
            per_device_train_batch_size=1,
            per_device_eval_batch_size=1,
            weight_decay=0.01,
            logging_steps=10,
            evaluation_strategy='steps',
            eval_steps=500,
            save_steps=1e6,
            gradient_accumulation_steps=16
        )

        # The params.yaml file also includes the same hyperparameters which can be used as shown below:

        # trainer_args = TrainingArguments(
        #     output_dir=self.config.root_dir,
        #     num_train_epochs=self.config.num_train_epochs,
        #     warmup_steps=self.config.warmup_steps,
        #     per_device_train_batch_size=self.config.per_device_train_batch_size,
        #     per_device_eval_batch_size=self.config.per_device_train_batch_size,
        #     weight_decay=self.config.weight_decay,
        #     logging_steps=self.config.logging_steps,
        #     evaluation_strategy=self.config.evaluation_strategy,
        #     eval_steps=self.config.eval_steps,
        #     save_steps=1e6,
        #     gradient_accumulation_steps=self.config.gradient_accumulation_steps
        # )

        train = Trainer(
            model=pegasus,
            args=trainer_args,
            tokenizer=tokenizer,
            data_collator=seq2seq_collator,
            train_dataset=dataset_samsum["train"],
            eval_dataset=dataset_samsum["validation"]
        )

        train.train()

        pegasus.save_pretrained(os.path.join(self.config.root_dir, "pegasus-samsum-model"))

        tokenizer.save_pretrained(os.path.join(self.config.root_dir, "tokenizer"))
        