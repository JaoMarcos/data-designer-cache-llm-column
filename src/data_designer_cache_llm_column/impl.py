import logging

from .cache_control import CacheControl
from .config import CacheLLMTextColumnConfig

# Data Designer uses the standard Python logging module for logging
logger = logging.getLogger(__name__)

# Make sure to import your generator base class correctly
from data_designer.engine.column_generators.generators.llm_completion import (
    ColumnGeneratorWithModelChatCompletion,
    LLMCodeCellGenerator,
    LLMJudgeCellGenerator,
    LLMStructuredCellGenerator,
    LLMTextCellGenerator,
)


class CacheLLMTextCellGenerator(
    ColumnGeneratorWithModelChatCompletion[CacheLLMTextColumnConfig]
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_control = CacheControl(storage_path=self.config.cache_folder)

    def generate(self, data: dict) -> dict:
        kwargs = self._prepare_generation_kwargs(data)
        console.log(f"Generation kwargs: {kwargs}")
        cached_result = self.cache_control.get_from_cache(kwargs)
        if cached_result is not None:
            response, trace = cached_result
        else:
            response, trace = self.model.generate(**kwargs)
            self.cache_control.save_to_cache(kwargs, (response, trace))

        return self._process_generation_result(data, response, trace)
