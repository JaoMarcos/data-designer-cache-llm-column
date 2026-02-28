from data_designer.plugins import Plugin, PluginType

plugin = Plugin(
    impl_qualified_name="data_designer_cache_llm_column.cache_llm_code_column.impl.CacheLLMCodeCellGenerator",
    config_qualified_name="data_designer_cache_llm_column.cache_llm_code_column.config.CacheLLMCodeColumnConfig",
    plugin_type=PluginType.COLUMN_GENERATOR,
    emoji="💾",
)
