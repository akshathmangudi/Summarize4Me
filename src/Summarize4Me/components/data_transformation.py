import os

from Summarize4Me.logging import logger
from Summarize4Me.entity import DataTransformationConfig
from transformers import AutoTokenizer
from datasets import load_dataset, load_from_disk


# This class will be responsible for handling the data transformation
# of the Pipeline
class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config=config
        self.tokenizer=AutoTokenizer.from_pretrained(config.tokenizer_path)

    def convert_to_features(self, batch):
        """
        This method will convert the text feeded to the method, and be converted as encodings/features.
        Input encodings are the feeded text and target encodings are the summary from that conversion.

        :param batch: The text feeded to the method.
        """
        input_encodings=self.tokenizer(batch['dialogue'], max_length=1024, truncation=True)

        with self.tokenizer.as_target_tokenizer():
            target_encodings=self.tokenizer(batch['summary'], max_length=240, truncation=True)

        return {
            'input_ids': input_encodings['input_ids'],
            'attention_mask': input_encodings['attention_mask'],
            'labels': input_encodings['input_ids']
        }

    def convert(self):
        """
        The transformed data is joined to the artifacts directory as a separate directory of its own.
        """
        dataset_samsum = load_from_disk(self.config.data_path)
        dataset_samsum_pt = dataset_samsum.map(self.convert_to_features, batched=True)
        dataset_samsum_pt.save_to_disk(os.path.join(self.config.root_dir, "samsum_dataset"))
