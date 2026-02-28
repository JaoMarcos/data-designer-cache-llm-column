from typing import Literal

from data_designer.config.column_configs import LLMTextColumnConfig

from ..config import CacheConfigBase


class CacheLLMTextColumnConfig(LLMTextColumnConfig, CacheConfigBase):
    """Configuration for the cache LLM text column generator."""

    column_type: Literal["cache-llm-text"] = "cache-llm-text"
