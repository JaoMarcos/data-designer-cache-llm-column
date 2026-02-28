import time

import data_designer.config as dd
import pandas as pd
from data_designer.config.seed_source_dataframe import DataFrameSeedSource
from data_designer.interface import DataDesigner

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
