from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI

context_persist_dir = "../data/storage_context"

llm = OpenAI(model="gpt-3.5-turbo")
# llm = Ollama(model="llama3.2:3b", request_timeout=120.0)

embed_model = OllamaEmbedding(model_name="nomic-embed-text")
# embed_model = OpenAIEmbedding(model_name="text-embedding-ada-002")
