from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.vector_stores.types import ExactMatchFilter, MetadataFilters

from database import get_pg_vector_store, get_candidates, update_candidate_summary
from models import llm, embed_model, context_persist_dir
from prompts import summary_prompt


# enable_debug_mode()


def get_summary(file_name: str, index: VectorStoreIndex) -> str:
    filters = MetadataFilters(
        filters=[
            ExactMatchFilter(key="file_name", value=file_name),
        ]
    )

    query_engine = index.as_query_engine(filters=filters, similarity_top_k=5, llm=llm)
    response = query_engine.query(summary_prompt)

    return str(response)


if __name__ == "__main__":
    # 6. generate experience summary
    candidates = get_candidates()
    vector_store = get_pg_vector_store()
    storage_context = StorageContext.from_defaults(persist_dir=context_persist_dir)

    index = VectorStoreIndex.from_vector_store(
        embed_model=embed_model,
        vector_store=vector_store,
        storage_context=storage_context,
    )

    for file_name, name, profession, years in candidates:
        summary = get_summary(file_name, index)
        update_candidate_summary(file_name, summary)

    print("Done!")
