import logging

from .cache_control import CacheControl

# Data Designer uses the standard Python logging module for logging
logger = logging.getLogger(__name__)

# Make sure to import your generator base class correctly

from typing import TYPE_CHECKING, Generic, TypeVar, get_origin

from data_designer.config.column_configs import (
    LLMCodeColumnConfig,
    LLMJudgeColumnConfig,
    LLMStructuredColumnConfig,
    LLMTextColumnConfig,
)
from data_designer.engine.column_generators.generators.llm_completion import (
    ColumnGeneratorWithModelChatCompletion,
    LLMStructuredCellGenerator,
)
from pydantic import BaseModel


class CacheLLMStructuredCellGenerator(LLMStructuredCellGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_control = CacheControl(storage_path=self.config.cache_folder)

    def generate(self, data: dict) -> dict:
        try:
            original_type = self.config.column_type
            self.config.column_type = (
                "llm-structured"  # Temporarily set to base type for generation
            )
            kwargs = self._prepare_generation_kwargs(data)

            cached_result = None
            if self.config.load_cache:
                cached_result = self.cache_control.get_from_cache(kwargs)
            if cached_result is not None:
                response = cached_result
                trace = None  # Cache may not have trace information
            else:
                response, trace = self.model.generate(**kwargs)
                if self.config.save_cache:
                    self.cache_control.save_to_cache(kwargs, response)

            pgr = self._process_generation_result(data, response, trace)
            self.config.column_type = original_type  # Restore the original column type
        except Exception as e:
            logger.error(f"Error during generation: {e}")
            raise
        return pgr
