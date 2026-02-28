import logging

from ..impl import ColumnGeneratorWithCacheModelChatCompletion
from .config import CacheLLMCodeColumnConfig

logger = logging.getLogger(__name__)


class CacheLLMCodeCellGenerator(
    ColumnGeneratorWithCacheModelChatCompletion[CacheLLMCodeColumnConfig]
): ...
