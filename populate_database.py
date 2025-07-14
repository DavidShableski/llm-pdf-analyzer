import argparse
import os
import shutil

from typing import List
from langchain.schema.document import Document

from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

from get_embedding_function import get_embedding_function

#dedicated chroma package
from langchain_chroma import Chroma

DATA_PATH   = "data"
CHROMA_PATH = "chroma"

def main() -> None:
    """
    CLI entrypoint: optionally reset, then load & index all PDF chunks.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()

    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    documents = load_documents(DATA_PATH)
    chunks    = split_documents(documents)
    add_to_chroma(chunks, CHROMA_PATH)

def load_documents(data_path: str) -> List[Document]:
    """
    Load all PDFs from `data_path` into LangChain Document objects.
    """
    loader = PyPDFDirectoryLoader(data_path)
    return loader.load()

def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split each Document into smaller text chunks for embedding.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return splitter.split_documents(documents)

def add_to_chroma(chunks: List[Document], chroma_path: str) -> None:
    """
    Persist new chunks into a Chroma vector store at `chroma_path`.
    """
    db = Chroma(
        persist_directory=chroma_path,
        embedding_function=get_embedding_function()
    )

    #calculate ids and remove duplicates
    existing    = db.get(include=[])
    existing_ids= set(existing["ids"])
    chunks_with_ids = calculate_chunk_ids(chunks)

    new_chunks = [
        c for c in chunks_with_ids
        if c.metadata["id"] not in existing_ids
    ]

    if new_chunks:
        print(f"Adding {len(new_chunks)} new chunks")
        ids = [c.metadata["id"] for c in new_chunks]
        db.add_documents(new_chunks, ids=ids)
        
        # if hasattr(db, "persist"):
        #     db.persist()
    else:
        print("No new documents to add")

    del db  #let python clean up any resources

def calculate_chunk_ids(chunks: List[Document]) -> List[Document]:
    """
    Assign a unique `id` metadata field to each chunk based on source+page.
    """
    last = None
    idx  = 0
    for chunk in chunks:
        src = chunk.metadata.get("source")
        pg  = chunk.metadata.get("page")
        key = f"{src}:{pg}"
        idx = idx + 1 if key == last else 0
        chunk.metadata["id"] = f"{key}:{idx}"
        last = key
    return chunks

def clear_database() -> None:
    """
    Delete the entire Chroma directory to reset the database.
    """
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

#expose for in-process import
__all__ = [
    "clear_database",
    "load_documents",
    "split_documents",
    "add_to_chroma",
]
