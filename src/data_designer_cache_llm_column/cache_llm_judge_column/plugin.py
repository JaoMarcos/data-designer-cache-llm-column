from data_designer.plugins import Plugin, PluginType

plugin = Plugin(
    impl_qualified_name="data_designer_cache_llm_column.cache_llm_judge_column.impl.CacheLLMJudgeCellGenerator",
    config_qualified_name="data_designer_cache_llm_column.cache_llm_judge_column.config.CacheLLMJudgeColumnConfig",
    plugin_type=PluginType.COLUMN_GENERATOR,
    emoji="💾",
)
