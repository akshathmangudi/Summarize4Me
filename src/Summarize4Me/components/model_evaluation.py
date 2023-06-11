from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset, load_from_disk, load_metric
import torch
import pandas
from tqdm import tqdm
from Summarize4Me.entity import ModelEvaluationConfig


# This class is responsible for generating the model evaluation (rouge scores) and the proper metric
# which will be helpful for hyperparameter tuning.
class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def generate_batch_chunks(self, list_elements, batch_size):
        """
        This is responsible for generating chunks from the list of elements fed to the method.

        :param list_elements: The total number of elements fed.
        :param batch_size: Separate the list of elements by batch_size.
        """
        for i in range(0, len(list_elements), batch_size):
            yield list_elements[i: i + batch_size]

    def calculate_metric(self, dataset, metric, model, tokenizer,
                         batch_size=16, device="cuda" if torch.cuda.is_available() else "cpu",
                         column_text="article",
                         column_summary="highlights"):

        """
        Responsible for calculating the model metric that will be used on model_trainer.py

        :param dataset: The dataset itself that will be used for calculating the metric.
        :param metric: The metric that will be used to evaluate the model, for example. For this program,
        we will use the rouge metric.
        :param model: The model that will be evaluated against the rouge metric.
        :param tokenizer: Tokenization is the process of chopping up sentences into pieces/tokens which cannot be
        divided further
        :param batch_size: The batch size that will split the entire dataset into 16-group chunks
        :param device: The device to be used by torch. (cpu/gpu)
        :param column_text: The input feature that's fed in
        :param column_summary: The output feature that will be received, which is a metric evaluation
        :return: Returns a score in a tabular format when evaluated against 3-4 types of rouge metric.
        """

        article_batches = list(self.generate_batch_chunks(dataset[column_text], batch_size))
        target_batches = list(self.generate_batch_chunks(dataset[column_summary], batch_size))

        for article_batch, target_batch in tqdm(
            zip(article_batches, target_batches), total=len(article_batches)):
            inputs = tokenizer(article_batch, max_length=2048, truncation=True, padding="max_length", return_tensors="pt")

            summaries = model.generate(input_ids=inputs["input_ids"].to(device), attention_mask=inputs["attention_mask"].to(device), length_penalty=0.8, num_beams=8, max_length=128)

            decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True, clean_up_tokenization_space=True) for s in summaries]

            decoded_summaries = [d.replace("", " ") for d in decoded_summaries]

            metric.add_batch(predictions=decoded_summaries, references=target_batch)

        score = metric.compute()
        return score

    def evaluate(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)

        dataset_samsum_pt = load_from_disk(self.config.data_path)

        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]

        rouge_metric = load_metric('rouge')

        score = self.calculate_metric(
            dataset_samsum_pt['test'][0:10], rouge_metric, pegasus, tokenizer, batch_size=2, column_text='dialogue', column_summary='summary'
        )

        rouge_dict = dict((rn, score[rn].mid.fmeasure) for rn in rouge_names)

        df = pandas.DataFrame(rouge_dict, index=['pegasus'])
        df.to_csv(self.config.metric_file_name, index=False)
