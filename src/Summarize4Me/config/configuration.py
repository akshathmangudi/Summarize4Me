from Summarize4Me.constants import *
from Summarize4Me.utils.common import read_yaml, create_dirs
from Summarize4Me.entity import DataIngestionConfig, \
                                DataValidationConfig, \
                                DataTransformationConfig, \
                                ModelTrainerConfig, \
                                ModelEvaluationConfig


class ConfigManager:
    def __init__(
            self,
            config_fpath=CONFIG_FILE_PATH,
            params_fpath=PARAMS_FILE_PATH
    ):
        self.config = read_yaml(config_fpath)
        self.params = read_yaml(params_fpath)

        create_dirs([self.config.artifacts_root])

    def get_ingestion(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_dirs([config.root_dir])

        data_ingestion = DataIngestionConfig(
            root_dir=config.root_dir,
            source_url=config.source_url,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )

        return data_ingestion

    def get_validation(self) -> DataValidationConfig:
        config = self.config.data_validation

        create_dirs([config.root_dir])

        data_validation_string = DataValidationConfig(
            root_dir=config.root_dir,
            status_file=config.status_file,
            required_files=config.required_files
        )

        return data_validation_string

    def data_trans_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        create_dirs([config.root_dir])

        data_trans_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            tokenizer_path=config.tokenizer_path
        )

        return data_trans_config

    def get_model_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params.TrainingArguments

        create_dirs([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            pretrained_model=config.pretrained_model,
            num_epochs=params.num_epochs,
            warmup_steps=params.warmup_steps,
            per_device_train_batch_size=params.per_device_train_batch_size,
            weight_decay=params.weight_decay,
            logging_steps=params.logging_steps,
            evaluation_strategy=params.evaluation_strategy,
            evaluation_steps=params.evaluation_strategy,
            save_steps=params.save_steps,
            accumulation_steps=params.accumulation_steps
        )

        return model_trainer_config

    def get_model_eval_cfg(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation

        create_dirs([config.root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            model_path=config.model_path,
            tokenizer_path=config.tokenizer_path,
            metric_file_name=config.metric_file_name
        )

        return model_evaluation_config
