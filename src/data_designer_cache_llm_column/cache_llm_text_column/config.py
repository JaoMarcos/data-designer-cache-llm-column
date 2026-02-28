from typing import TYPE_CHECKING, Generic, Literal, TypeVar, get_origin

from data_designer.config.column_configs import (
    LLMCodeColumnConfig,
    LLMJudgeColumnConfig,
    LLMStructuredColumnConfig,
    LLMTextColumnConfig,
)
from pydantic import Field

from ..config import CacheConfigBase


class CacheLLMTextColumnConfig(LLMTextColumnConfig, CacheConfigBase):
    """Configuration for the cache LLM text column generator."""

    column_type: Literal["cache-llm-text"] = "cache-llm-text"
