#run $env:PYTHONPATH = $PWD
import pytest
from langchain.schema import Document
from populate_database import split_documents

def test_split_documents_simple():
    #create one “page” of 2000 characters
    long_text = "A" * 2000
    doc = Document(page_content=long_text, metadata={"source": "dummy.pdf", "page": 0})

    chunks = split_documents([doc])

    #we expect more than one chunk
    assert len(chunks) > 1

    #none of the chunks should exceed the default chunk size of 800
    assert all(len(c.page_content) <= 800 for c in chunks)

    #and each chunk should carry through its metadata.source and metadata.page
    assert all(chunk.metadata["source"] == "dummy.pdf" for chunk in chunks)
    assert all(chunk.metadata["page"] == 0            for chunk in chunks)
