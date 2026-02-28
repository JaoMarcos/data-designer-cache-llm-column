from typing import Literal

from data_designer.config.column_configs import LLMJudgeColumnConfig

from ..config import CacheConfigBase


class CacheLLMJudgeColumnConfig(LLMJudgeColumnConfig, CacheConfigBase):
    """Configuration for the cache LLM judge column generator."""

    column_type: Literal["cache-llm-judge"] = "cache-llm-judge"
