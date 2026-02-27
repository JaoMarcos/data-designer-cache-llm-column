from data_designer.plugins import Plugin, PluginType

# Plugin instance - this is what gets loaded via entry point
plugin = Plugin(
    impl_qualified_name="data_designer_cache_llm_column.impl.CacheLLMTextCellGenerator",
    # Notice the change here to point to config.py
    config_qualified_name="data_designer_cache_llm_column.config.CacheLLMTextColumnConfig",
    plugin_type=PluginType.COLUMN_GENERATOR,
    emoji="💾",
)
