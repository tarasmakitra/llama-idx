from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.vector_stores.types import ExactMatchFilter, MetadataFilters

from database import get_pg_vector_store
from models import llm, embed_model, context_persist_dir


def get_persisted_vector_index() -> VectorStoreIndex:
    vector_store = get_pg_vector_store()
    storage_context = StorageContext.from_defaults(persist_dir=context_persist_dir)

    return VectorStoreIndex.from_vector_store(
        embed_model=embed_model,
        vector_store=vector_store,
        storage_context=storage_context,
    )


def get_candidate_query_engine(
    index: VectorStoreIndex, file_name: str
) -> BaseQueryEngine:
    filters = MetadataFilters(
        filters=[
            ExactMatchFilter(key="file_name", value=file_name),
        ]
    )

    return index.as_query_engine(filters=filters, similarity_top_k=5, llm=llm)
