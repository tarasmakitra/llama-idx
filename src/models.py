import os

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

load_dotenv()

context_persist_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../data/storage_context")
)

# llm = OpenAI(model="gpt-4o-mini")
# embed_model = OpenAIEmbedding(model_name="text-embedding-ada-002")

azure_endpoint = "https://agentic-ai-learning-bench.cognitiveservices.azure.com/"
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

llm = AzureOpenAI(
    model="gpt-4o-mini",
    deployment_name="gpt-4o-mini",
    api_version="2024-12-01-preview",
    azure_endpoint=azure_endpoint,
    azure_ad_token_provider=token_provider,
    use_azure_ad=True,
)

embed_model = AzureOpenAIEmbedding(
    model="text-embedding-3-small",
    deployment_name="text-embedding-3-small",
    api_version="2024-02-01",
    azure_endpoint=azure_endpoint,
    azure_ad_token_provider=token_provider,
    use_azure_ad=True,
)

# from llama_index.embeddings.ollama import OllamaEmbedding
# from llama_index.llms.ollama import Ollama

# llm = OpenAI(model="gpt-4o-mini")
# llm = OpenAI(model="gpt-3.5-turbo")
# llm = Ollama(model="llama3.2:3b", request_timeout=120.0)
# embed_model = OllamaEmbedding(model_name="nomic-embed-text")
