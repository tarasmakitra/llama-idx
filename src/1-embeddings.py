import json
import os
import shutil

import kagglehub
from llama_index.core import (
    Document,
    VectorStoreIndex,
)
from llama_index.core import (
    StorageContext,
)
from llama_index.core.node_parser import SentenceSplitter

from data import data_input_dir, read_directory, extract_json_from_text
from database import (
    create_candidates_table,
    save_candidate_details,
)
from database import (
    create_database,
    get_pg_vector_store,
)
from models import context_persist_dir
from models import llm, embed_model
from prompts import details_prompt


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


def retrieve_details(doc: Document):
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


if __name__ == "__main__":
    # 1. Download CV files
    download_dataset(data_input_dir)

    # 2-4. Generate embeddings and store in vector database
    documents = read_directory(input_dir=data_input_dir, num_files_limit=20)
    generate_embeddings(documents)

    # 5. Extract details from each document
    create_candidates_table()
    for document in documents:
        retrieve_details(document)

    print("Done!")
