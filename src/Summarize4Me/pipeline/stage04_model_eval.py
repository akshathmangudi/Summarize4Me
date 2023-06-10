from Summarize4Me.config.configuration import ConfigManager
from Summarize4Me.components.model_evaluation import ModelEvaluation
from Summarize4Me.logging import logger


class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigManager()
        model_eval_config = config.get_model_eval_cfg()
        model_eval_config = ModelEvaluation(config=model_eval_config)
        model_eval_config.evaluate()
