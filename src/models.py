import os
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

context_persist_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../data/storage_context")
)

llm = OpenAI(model="gpt-4.1")
# llm = OpenAI(model="gpt-4o-mini")
# llm = OpenAI(model="gpt-3.5-turbo")
# llm = Ollama(model="llama3.2:3b", request_timeout=120.0)

embed_model = OllamaEmbedding(model_name="nomic-embed-text")
# embed_model = OpenAIEmbedding(model_name="text-embedding-ada-002")
