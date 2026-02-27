from data_designer.config.column_configs import LLMTextColumnConfig
from pydantic import Field

class CacheLLMTextColumnConfig(LLMTextColumnConfig):
    """Configuration for the cache LLM column generator."""
    # Optional cache folder path to store the results of the function
    cache_folder: str = "cache_folder"