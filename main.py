from Summarize4Me.pipeline.stage00_ingestion import TrainingPipeline
from Summarize4Me.logging import logger

STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f"----{STAGE_NAME} started ----")
    data_ingestion = TrainingPipeline()
    data_ingestion.main()
    logger.info(f"----{STAGE_NAME} completed ----")
except Exception as e:
    logger.exception(e)
    raise e