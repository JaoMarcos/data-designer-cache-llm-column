import time

import data_designer.config as dd
import pandas as pd
from data_designer.config.seed_source_dataframe import DataFrameSeedSource
from data_designer.interface import DataDesigner
from pydantic import BaseModel

from data_designer_cache_llm_column.cache_llm_structured_column.config import (
    CacheLLMStructuredColumnConfig,
)
from data_designer_cache_llm_column.cache_llm_text_column.config import (
    CacheLLMTextColumnConfig,
)

seed_df = pd.DataFrame({"language": ["English", "Spanish", "French"]})

config_builder = dd.DataDesignerConfigBuilder()
config_builder.with_seed_dataset(DataFrameSeedSource(df=seed_df))

config_builder.add_column(
    CacheLLMTextColumnConfig(
        name="greeting",
        model_alias="nvidia-text",
        prompt="Write a casual {{ language }}. one sentence",
        cache_folder="./llm_cache_storage",
        save_cache=True,
        load_cache=False,  # Set to False for testing to ensure cache is bypassed on first run
    )
)

data_designer = DataDesigner()

print("--- Run 1: Calling Model API ---")
t0 = time.perf_counter()
results1 = data_designer.preview(config_builder, num_records=3)
t1 = time.perf_counter()
print(f"Time: {t1 - t0:.2f}s")
print(results1.dataset)

config_builder = dd.DataDesignerConfigBuilder()
config_builder.with_seed_dataset(DataFrameSeedSource(df=seed_df))

config_builder.add_column(
    CacheLLMTextColumnConfig(
        name="greeting",
        model_alias="nvidia-text",
        prompt="Write a casual {{ language }}. one sentence",
        cache_folder="./llm_cache_storage",
        save_cache=True,
        load_cache=True,  # Set to True to load from cache on subsequent runs
    )
)


print("\n--- Run 2: Loading from Cache ---")
t2 = time.perf_counter()
results2 = data_designer.preview(config_builder, num_records=3)
t3 = time.perf_counter()
print(f"Time: {t3 - t2:.2f}s")
print(results2.dataset)

print(f"\n--- Speedup: {(t1 - t0) / (t3 - t2):.1f}x faster from cache ---")

for r1, r2 in zip(results1.dataset["greeting"], results2.dataset["greeting"]):
    assert r1 == r2, "Cached result does not match original result"


# --- CacheLLMStructuredColumnConfig example ---


class GreetingInfo(BaseModel):
    greeting: str
    formality: str


seed_df2 = pd.DataFrame({"language": ["English", "Spanish", "French"]})

config_builder3 = dd.DataDesignerConfigBuilder()
config_builder3.with_seed_dataset(DataFrameSeedSource(df=seed_df2))

config_builder3.add_column(
    CacheLLMStructuredColumnConfig(
        name="greeting_info",
        model_alias="nvidia-text",
        prompt="Generate a greeting in {{ language }} and classify its formality level.",
        output_format=GreetingInfo,
        cache_folder="./llm_cache_storage_structured",
        save_cache=True,
        load_cache=False,
    )
)

print("\n--- Structured Run 1: Calling Model API ---")
t4 = time.perf_counter()
results3 = data_designer.preview(config_builder3, num_records=3)
t5 = time.perf_counter()
print(f"Time: {t5 - t4:.2f}s")
print(results3.dataset)


config_builder4 = dd.DataDesignerConfigBuilder()
config_builder4.with_seed_dataset(DataFrameSeedSource(df=seed_df2))

config_builder4.add_column(
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

print("\n--- Structured Run 2: Loading from Cache ---")
t6 = time.perf_counter()
results4 = data_designer.preview(config_builder4, num_records=3)
t7 = time.perf_counter()
print(f"Time: {t7 - t6:.2f}s")
print(results4.dataset)
results4.display_sample_record(index=0)

print(f"\n--- Structured Speedup: {(t5 - t4) / (t7 - t6):.1f}x faster from cache ---")

for r3, r4 in zip(results3.dataset["greeting_info"], results4.dataset["greeting_info"]):
    assert r3 == r4, "Cached structured result does not match original result"
