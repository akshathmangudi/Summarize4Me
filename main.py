from Summarize4Me.pipeline.stage00_ingestion import IngestionTrainingPipeline
from Summarize4Me.pipeline.stage01_validation import ValidationTrainingPipeline
from Summarize4Me.pipeline.stage02_transformation import TransformationTrainingPipeline
from Summarize4Me.logging import logger

STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f"----{STAGE_NAME} started ----")
    data_ingestion = IngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f"----{STAGE_NAME} completed ----")
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = "Data Validation Stage"

try:
    logger.info(f"----{STAGE_NAME} started ----")
    data_validation = ValidationTrainingPipeline()
    data_validation.main()
    logger.info(f"----{STAGE_NAME} completed ----")
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = "Data Transformation Stage"

try:
    logger.info(f"----{STAGE_NAME} started ----")
    data_transformation = TransformationTrainingPipeline()
    data_transformation.main()
    logger.info(f"----{STAGE_NAME} completed ----")
except Exception as e:
    logger.exception(e)
    raise e