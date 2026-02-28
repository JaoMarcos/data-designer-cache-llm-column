from typing import Literal

from data_designer.config.column_configs import LLMCodeColumnConfig

from ..config import CacheConfigBase


class CacheLLMCodeColumnConfig(LLMCodeColumnConfig, CacheConfigBase):
    """Configuration for the cache LLM code column generator."""

    column_type: Literal["cache-llm-code"] = "cache-llm-code"
