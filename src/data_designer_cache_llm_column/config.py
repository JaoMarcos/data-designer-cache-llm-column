from typing import Literal

from pydantic import BaseModel, Field


class CacheConfigBase(BaseModel):
    """Base configuration for cache-enabled LLM columns."""

    # Optional cache folder path to store the results of the function
    cache_folder: str = "cache_folder"
    cache_backend: Literal["pickle", "duckdb"] = Field(
        default="pickle",
        description="Storage backend for the cache. 'pickle' stores each entry as a separate file; 'duckdb' stores all entries in a single DuckDB database file.",
    )
    save_cache: bool = Field(
        default=True,
        description="Whether to save to cache for this column. If False, results will not be saved to cache, but the cache will still be checked and loaded if use_cache is True.",
    )
    load_cache: bool = Field(
        default=True,
        description="Whether to load from cache for this column. If False, the cache will be bypassed and the model will be called every time, but results will still be saved to cache ifsave_cache is True.",
    )
