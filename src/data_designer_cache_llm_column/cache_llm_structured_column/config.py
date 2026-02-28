from typing import TYPE_CHECKING, Generic, Literal, TypeVar, get_origin

from data_designer.config.column_configs import (
    LLMCodeColumnConfig,
    LLMJudgeColumnConfig,
    LLMStructuredColumnConfig,
    LLMTextColumnConfig,
)
from pydantic import Field

from ..config import CacheConfigBase


class CacheLLMStructuredColumnConfig(LLMStructuredColumnConfig, CacheConfigBase):
    """Configuration for the cache LLM structured column generator."""

    column_type: Literal["cache-llm-structured"] = "cache-llm-structured"
