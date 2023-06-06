from Summarize4Me.config.configuration import ConfigManager
from Summarize4Me.components.data_validation import DataValidation
from Summarize4Me.logging import logger


class ValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigManager()
        data_validation_config = config.get_validation()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_existence()
