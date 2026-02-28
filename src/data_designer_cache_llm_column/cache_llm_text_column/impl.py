import logging

from data_designer.engine.column_generators.generators.llm_completion import (
    LLMTextCellGenerator,
)

from ..cache_control import CacheControl
from ..impl import ColumnGeneratorWithCacheModelChatCompletion
from .config import CacheLLMTextColumnConfig

logger = logging.getLogger(__name__)


class CacheLLMTextCellGenerator(
    ColumnGeneratorWithCacheModelChatCompletion[CacheLLMTextColumnConfig]
): ...
