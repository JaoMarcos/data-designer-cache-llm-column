from typing import Literal

from data_designer.config.column_configs import LLMStructuredColumnConfig

from ..config import CacheConfigBase


class CacheLLMStructuredColumnConfig(LLMStructuredColumnConfig, CacheConfigBase):
    """Configuration for the cache LLM structured column generator."""

    column_type: Literal["cache-llm-structured"] = "cache-llm-structured"
