#run $env:PYTHONPATH = $PWD
import pytest
from langchain.schema import Document
from analyzer import query_rag

#a fake chroma vector store that returns two dummy docs
class DummyChroma:
    def __init__(self, persist_directory, embedding_function):
        pass
    def similarity_search_with_score(self, question, k):
        docs = [
            Document(page_content="First chunk", metadata={"id": "dummy.pdf:0:0"}),
            Document(page_content="Second chunk", metadata={"id": "dummy.pdf:1:0"}),
        ]
        scores = [0.95, 0.92]
        return list(zip(docs, scores))

#a fake LLM that always returns “TEST ANSWER”
class DummyLLM:
    def __init__(self, model):
        pass
    def invoke(self, prompt):
        return "TEST ANSWER"

@pytest.fixture(autouse=True)
def patch_chroma_and_llm(monkeypatch):
    #replace chroma in the analyzer module with our dummy
    monkeypatch.setattr("analyzer.Chroma", DummyChroma)
    #replace ollamaLLM in the analyzer module with our dummy
    monkeypatch.setattr("analyzer.OllamaLLM", DummyLLM)

def test_query_rag_returns_expected(monkeypatch):
    answer, sources = query_rag("any question", "unused_path")

    #the dummy LLM always returns this
    assert answer == "TEST ANSWER"

    #we expect the list of ids we set in the dummy docs
    assert sources == ["dummy.pdf:0:0", "dummy.pdf:1:0"]

def test_query_rag_fallback_branch(monkeypatch):
    # DummyChroma yields low scores below your threshold
    class LowScoreChroma:
        def __init__(self, persist_directory, embedding_function): pass
        def similarity_search_with_score(self, question, k):
            docs = [Document(page_content="A", metadata={"id": "x:0:0"})]
            scores = [0.1]  # below 0.7 threshold
            return list(zip(docs, scores))
    monkeypatch.setattr("analyzer.Chroma", LowScoreChroma)
    # Dummy LLM stays the same
    answer, sources = query_rag("q", "p")
    # It should still return something (fallback), and the source should match:
    assert sources == ["x:0:0"]
    assert isinstance(answer, str)