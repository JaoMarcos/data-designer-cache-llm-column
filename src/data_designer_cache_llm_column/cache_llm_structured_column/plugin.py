from data_designer.plugins import Plugin, PluginType

# Plugin instance - this is what gets loaded via entry point
plugin = Plugin(
    impl_qualified_name="data_designer_cache_llm_column.cache_llm_structured_column.impl.CacheLLMStructuredCellGenerator",
    # Notice the change here to point to config.py
    config_qualified_name="data_designer_cache_llm_column.cache_llm_structured_column.config.CacheLLMStructuredColumnConfig",
    plugin_type=PluginType.COLUMN_GENERATOR,
    emoji="💾",
)
