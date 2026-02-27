import logging
from data_designer.plugins import Plugin, PluginType

# Make sure to import your generator base class correctly
from data_designer.engine.column_generators.generators.llm_completion import (
    LLMCodeCellGenerator,
    LLMJudgeCellGenerator,
    LLMStructuredCellGenerator,
    LLMTextCellGenerator,
)
from .cache_control import CacheControl

# Data Designer uses the standard Python logging module for logging
logger = logging.getLogger(__name__)

class CacheLLMTextCellGenerator(LLMTextCellGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_control = CacheControl(storage_path=self.config.cache_folder)

    def generate(self, data: dict) -> dict:
        kwargs = self._prepare_generation_kwargs(data)
        
        cached_result = self.cache_control.get_from_cache(kwargs)
        if cached_result is not None:
            response, trace = cached_result
        else:
            response, trace = self.model.generate(**kwargs)
            self.cache_control.save_to_cache(kwargs, (response, trace))
            
        return self._process_generation_result(data, response, trace)

# Plugin instance - this is what gets loaded via entry point
plugin = Plugin(
    impl_qualified_name="data_designer_cache_llm_column.plugin.CacheLLMTextCellGenerator",
    # Notice the change here to point to config.py
    config_qualified_name="data_designer_cache_llm_column.config.CacheLLMTextColumnConfig",
    plugin_type=PluginType.COLUMN_GENERATOR,
    emoji="💾",
)