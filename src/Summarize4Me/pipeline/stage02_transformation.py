from Summarize4Me.config.configuration import ConfigManager
from Summarize4Me.components.data_transformation import DataTransformation
from Summarize4Me.logging import logger


class TransformationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigManager()
        data_transformation_config = config.data_trans_config()
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.convert()
