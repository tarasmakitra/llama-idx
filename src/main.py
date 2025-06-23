import json
import os
import shutil

import kagglehub
from llama_index.core import (
    Document,
)
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

from data import data_input_dir, read_directory, extract_json_from_text
from database import (
    create_candidates_table,
    save_candidate_details,
    create_database,
    get_pg_vector_store,
    update_candidate_summary,
)
from models import llm, embed_model, context_persist_dir
from prompts import details_prompt, summary_prompt
from schema import Candidate
from vector_index import get_persisted_vector_index, get_candidate_query_engine
from dotenv import load_dotenv

load_dotenv()
# enable_debug_mode()

cv_num_files_limit = int(os.getenv("NUM_FILES_LIMIT", 20))


def download_dataset(destination_path: str) -> None:
    dataset_path = kagglehub.dataset_download("snehaanbhawal/resume-dataset")

    try:
        if os.path.isdir(destination_path):
            shutil.rmtree(destination_path)

        shutil.copytree(
            os.path.join(dataset_path, "data", "data", "ENGINEERING"),
            destination_path,
        )
    except:
        print("An exception occurred while copying the dataset files.")
        exit(1)


def generate_embeddings(documents: list[Document]) -> None:
    create_database()
    vector_store = get_pg_vector_store()

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        embed_model=embed_model,
        transformations=[
            SentenceSplitter(chunk_size=256, chunk_overlap=32),
        ],
        show_progress=True,
    )

    index.storage_context.persist(persist_dir=context_persist_dir)


def retrieve_details_with_prompt(doc: Document):
    file_name = doc.metadata.get("file_name")
    response = llm.complete(details_prompt.format(text=doc.text))

    print(f"llm response for {file_name}:", response)

    try:
        data = json.loads(extract_json_from_text(str(response)))
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON for {file_name}: {e}")
        data = {}

    data["file_name"] = file_name

    save_candidate_details(data)

    print("Done parsing", file_name)


def retrieve_details_with_structured_llm(doc: Document):
    file_name = doc.metadata.get("file_name")
    sllm = llm.as_structured_llm(Candidate)

    response = sllm.complete(doc.text)

    print(f"candidate's details from {file_name}:", response)

    try:
        data = json.loads(extract_json_from_text(str(response)))
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON for {file_name}: {e}")
        data = {}

    data["file_name"] = file_name

    save_candidate_details(data)


def retrieve_candidate_summary(index: VectorStoreIndex, document: Document) -> None:
    file_name = document.metadata.get("file_name")
    query_engine = get_candidate_query_engine(index, file_name)
    summary = query_engine.query(summary_prompt)
    update_candidate_summary(file_name, str(summary))
    print(f"candidate's summary from {file_name}:", summary)


if __name__ == "__main__":
    # 1. Download CV files
    # download_dataset(data_input_dir)

    # 2-4. Generate embeddings and store in vector database
    documents = read_directory(input_dir=data_input_dir, num_files_limit=20)
    generate_embeddings(documents)
    print("Done generating embeddings")

    # 5. Extract details from each document
    create_candidates_table()
    for document in documents:
        # retrieve_details_with_prompt(document)
        retrieve_details_with_structured_llm(document)

    print("Done extracting details")

    # 6. Generate experience summary
    index = get_persisted_vector_index()
    for document in documents:
        retrieve_candidate_summary(index, document)

    print("Done extracting summary")

    print("Done!")
