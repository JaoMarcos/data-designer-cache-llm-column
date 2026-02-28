# data-designer-cache-llm-column

A plugin for `data-designer` that adds cache-enabled LLM column generators.

## Why use it?

When building datasets with `data-designer` using Large Language Models (LLMs), generation can be slow and expensive. When iterating on your data pipelines or prompts, you often end up running the exact same model calls multiple times.

This plugin automatically caches your LLM responses locally so that subsequent runs with identical inputs (prompt, variables, model) are instantaneous. This significantly speeds up dataset generation during development and reduces your overall LLM API costs.

## Features

- **Drop-in replacements**: Wraps the existing `data-designer` LLM columns (`Text`, `Structured`, `Code`, `Judge`) with caching capabilities.
- **Cost and Time Savings**: Avoids redundant LLM API calls by saving responses locally.
- **Flexible Cache Control**: Independently control whether to load from cache or save to cache for each column.

## Installation

Install using `pip`:

```bash
pip install data-designer-cache-llm-column
```

Or using `uv` (recommended):

```bash
uv pip install data-designer-cache-llm-column
```

## Available Column Types

This plugin exposes four new cache-enabled column configurations:

- `CacheLLMTextColumnConfig` (Type: `"cache-llm-text"`)
- `CacheLLMStructuredColumnConfig` (Type: `"cache-llm-structured"`)
- `CacheLLMCodeColumnConfig` (Type: `"cache-llm-code"`)
- `CacheLLMJudgeColumnConfig` (Type: `"cache-llm-judge"`)

## Configuration Options

All cached columns inherit from their respective base `data-designer` column configs, meaning you can still use parameters like `name`, `model_alias`, `prompt`, etc. In addition, you get these caching-specific options:

- `cache_folder` (`str`): The folder path where cache files will be stored. Default is `"cache_folder"`.
- `save_cache` (`bool`): Whether to save new LLM responses to the cache. Default is `True`.
- `load_cache` (`bool`): Whether to attempt loading from the cache before calling the LLM API. Default is `True`. By setting this to `False` and `save_cache` to `True`, you can force the model to re-generate and overwrite the cache.

## Example Usage

### Caching LLM Text Output

```python
import data_designer.config as dd
import pandas as pd
from data_designer.config.seed_source_dataframe import DataFrameSeedSource
from data_designer.interface import DataDesigner

from data_designer_cache_llm_column.cache_llm_text_column.config import CacheLLMTextColumnConfig

# Create seed dataset
seed_df = pd.DataFrame({"language": ["English", "Spanish", "French"]})

config_builder = dd.DataDesignerConfigBuilder()
config_builder.with_seed_dataset(DataFrameSeedSource(df=seed_df))

# Add a cached LLM text column
config_builder.add_column(
    CacheLLMTextColumnConfig(
        name="greeting",
        model_alias="nvidia-text", # Or whatever model alias you have configured
        prompt="Write a casual {{ language }} greeting. One sentence only.",
        cache_folder="./llm_cache_storage",
        save_cache=True,
        load_cache=True, # Hits the API on 1st run, loads from cache on subsequent runs
    )
)

data_designer = DataDesigner()

# First run: Hits the Model API and saves to cache
print("Run 1: Generating...")
results1 = data_designer.preview(config_builder, num_records=3)
print(results1.dataset)

# Second run: Instantly loads from cache
print("Run 2: Loading from cache...")
results2 = data_designer.preview(config_builder, num_records=3)
print(results2.dataset)
```

### Caching Structured Output

```python
import data_designer.config as dd
import pandas as pd
from data_designer.config.seed_source_dataframe import DataFrameSeedSource
from data_designer.interface import DataDesigner
from pydantic import BaseModel

from data_designer_cache_llm_column.cache_llm_structured_column.config import CacheLLMStructuredColumnConfig

# Define your expected output structure
class GreetingInfo(BaseModel):
    greeting: str
    formality: str

seed_df = pd.DataFrame({"language": ["English", "Spanish", "French"]})

config_builder = dd.DataDesignerConfigBuilder()
config_builder.with_seed_dataset(DataFrameSeedSource(df=seed_df))

# Add a cached LLM structured column
config_builder.add_column(
    CacheLLMStructuredColumnConfig(
        name="greeting_info",
        model_alias="nvidia-text",
        prompt="Generate a greeting in {{ language }} and classify its formality level.",
        output_format=GreetingInfo,
        cache_folder="./llm_cache_storage_structured",
        save_cache=True,
        load_cache=True,
    )
)

data_designer = DataDesigner()
results = data_designer.preview(config_builder, num_records=3)
print(results.dataset)
```
