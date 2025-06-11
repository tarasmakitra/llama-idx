from llama_index.core.tools import QueryEngineTool
from llama_index.core.vector_stores.types import ExactMatchFilter, MetadataFilters

from models import llm
from vector_index import get_persisted_vector_index

index = get_persisted_vector_index()


def create_query_engine_tool(file_name: str) -> QueryEngineTool:
    filters = MetadataFilters(
        filters=[
            ExactMatchFilter(key="file_name", value=file_name),
        ]
    )

    query_engine = index.as_query_engine(filters=filters, similarity_top_k=5, llm=llm)

    return QueryEngineTool.from_defaults(
        query_engine=query_engine,
        name="candidate_details",
        description=(
            "Provides information about the candidate."
            "Use a detailed plain text question as input to the tool."
        ),
    )


query_engine_tool = create_query_engine_tool("10030015.pdf")
