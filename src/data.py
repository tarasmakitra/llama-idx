import json
import re
from llama_index.core import (
    SimpleDirectoryReader,
    Document,
)

data_input_dir = "../data/csv"


def read_directory(
    input_dir: str, num_files_limit: int = 25, num_workers: int = 1
) -> list[Document]:
    reader = SimpleDirectoryReader(
        input_dir=input_dir,
        num_files_limit=num_files_limit,
        required_exts=[".pdf"],
        recursive=True,
    )

    return reader.load_data(num_workers=num_workers)


def extract_json_from_text(response: str):
    # remove markdown code block markers
    match = re.search(r"```json\s*(\{.*?\})\s*```", response, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # fallback: try to find any JSON object in the string
        match = re.search(r"(\{.*\})", response, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            raise ValueError("No JSON object found in response")
    return json_str
