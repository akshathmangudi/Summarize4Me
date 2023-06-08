from Summarize4Me.config.configuration import ConfigManager
from Summarize4Me.components.model_trainer import ModelTrainer
from Summarize4Me.logging import logger

class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigManager()
            model_trainer_config = config.get_model_config()
            model_trainer_config = ModelTrainer(config=model_trainer_config)
            model_trainer_config.train()
        except Exception as e:
            raise e