from Summarize4Me.constants import *
from Summarize4Me.utils.common import read_yaml, create_dirs
from Summarize4Me.entity import DataIngestionConfig, DataValidationConfig

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
    