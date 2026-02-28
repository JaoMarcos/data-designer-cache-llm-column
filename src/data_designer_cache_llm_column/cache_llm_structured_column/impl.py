from data_designer.engine.column_generators.generators.llm_completion import (
    LLMStructuredColumnConfig,
    LLMTextCellGenerator,
)

from ..cache_control import CacheControl
from ..impl import ColumnGeneratorWithCacheModelChatCompletion
from .config import CacheLLMStructuredColumnConfig

logger = logging.getLogger(__name__)


class CacheLLMStructuredCellGenerator(
    ColumnGeneratorWithCacheModelChatCompletion[CacheLLMStructuredColumnConfig]
):
    def _process_serialized_output(self, serialized_output: str) -> dict | list:
        return deserialize_json_values(serialized_output)
