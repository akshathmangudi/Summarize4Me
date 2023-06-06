import os
from Summarize4Me.logging import logger
from Summarize4Me.entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config=config

    def validate_existence(self)-> bool:
        try:
            val_status = None
            all_files = os.listdir(os.path.join("artifacts", "data_ingestion", "samsum_dataset"))

            for file in all_files:
                if file not in self.config.required_files:
                    val_status = False
                    with open(self.config.status_file, 'w') as f:
                        f.write(f"Validation status: {val_status}")
                else:
                    val_status = True
                    with open(self.config.status_file, 'w') as f:
                        f.write(f"Validation status: {val_status}")
            return val_status
        except Exception as e:
            raise e
