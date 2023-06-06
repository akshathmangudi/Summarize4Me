from Summarize4Me.config.configuration import ConfigManager
from Summarize4Me.components.data_ingestion import DataIngestion
from Summarize4Me.logging import logger


class IngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigManager()
        data_ingestion_config = config.get_ingestion()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip()
