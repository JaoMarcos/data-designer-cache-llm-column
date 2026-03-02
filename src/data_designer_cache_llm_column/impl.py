import logging

from data_designer.config.column_configs import LLMTextColumnConfig
from data_designer.engine.column_generators.generators.llm_completion import (
    ColumnGeneratorWithModelChatCompletion,
)
from data_designer.engine.configurable_task import TaskConfigT

from .cache_control import CacheControl, DuckDBCacheControl

logger = logging.getLogger(__name__)


class ColumnGeneratorWithCacheModelChatCompletion(
    ColumnGeneratorWithModelChatCompletion[TaskConfigT]
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.config.cache_backend == "duckdb":
            self.cache_control = DuckDBCacheControl(
                storage_path=self.config.cache_folder
            )
        else:
            self.cache_control = CacheControl(storage_path=self.config.cache_folder)

    def generate(self, data: dict) -> dict:
        try:
            self.super_type = super().config.column_type
            original_type = self.config.column_type
            self.config.column_type = "-".join(
                self.config.column_type.split("-")[1:]
            )  # Temporarily set to base type for generation
            kwargs = self._prepare_generation_kwargs(data)
            kwargs["_model"] = self.config.model_alias
            cached_result = None
            trace = None
            if self.config.load_cache:
                cached_result = self.cache_control.get_from_cache(kwargs)

            if cached_result is not None:
                response, trace = cached_result
            else:
                response, trace = self.model.generate(**kwargs)
                if self.config.save_cache:
                    self.cache_control.save_to_cache(kwargs, (response, trace))

            pgr = self._process_generation_result(data, response, trace)
            self.config.column_type = original_type  # Restore the original column type
        except Exception as e:
            logger.error(f"Error during generation: {e}")
            raise
        return pgr
