import data_designer.config as dd
from data_designer.interface import DataDesigner

# Import the custom caching config from the local package
from data_designer_cache_llm_column.config import CacheLLMTextColumnConfig

def main():
    # 1. Initialize DataDesigner
    data_designer = DataDesigner()
    config_builder = dd.DataDesignerConfigBuilder()

    # 2. Add a sampler column to provide variables for the prompt
    config_builder.add_column(
        dd.SamplerColumnConfig(
            name="language",
            sampler_type=dd.SamplerType.CATEGORY,
            params=dd.CategorySamplerParams(
                values=["English", "Spanish", "French"],
            ),
        )
    )

    # 3. Add the Cache LLM Text column
    # Notice we're using CacheLLMTextColumnConfig instead of standard LLMTextColumnConfig.
    # We specify the cache_folder where pickle files will be saved.
    config_builder.add_column(
        CacheLLMTextColumnConfig(
            name="greeting",
            model_alias="nvidia-text", # e.g. "openai-gpt-4o" or a mock model if testing
            prompt="Write a casual and formal greeting in {{ language }}.",
            cache_folder="./llm_cache_storage"
        )
    )

    print("--- First Run: Generating (Calling Model API) ---")
    results1 = data_designer.preview(config_builder)
    results1.display_sample_record()

    # If you run preview again (or full generation), it will use the identical kwargs 
    # to hash the request and load the response and trace from the `./llm_cache_storage` directory
    # instead of calling the model endpoint again.
    
    print("--- Second Run: Fetching from Cache (Skipping API) ---")
    results2 = data_designer.preview(config_builder)
    results2.display_sample_record()

if __name__ == "__main__":
    main()
