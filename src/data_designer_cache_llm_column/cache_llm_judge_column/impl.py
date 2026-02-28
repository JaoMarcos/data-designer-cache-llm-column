import logging

from data_designer.engine.processing.utils import deserialize_json_values

from ..impl import ColumnGeneratorWithCacheModelChatCompletion
from .config import CacheLLMJudgeColumnConfig

logger = logging.getLogger(__name__)


class CacheLLMJudgeCellGenerator(
    ColumnGeneratorWithCacheModelChatCompletion[CacheLLMJudgeColumnConfig]
):
    def _process_serialized_output(self, serialized_output: str) -> dict | list:
        return deserialize_json_values(serialized_output)
