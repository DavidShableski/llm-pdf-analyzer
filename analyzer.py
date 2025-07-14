from typing import Tuple, List
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from get_embedding_function import get_embedding_function
from langchain.prompts import ChatPromptTemplate

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def query_rag(question: str, chroma_path: str) -> Tuple[str, List[str]]:
    """
     Run a similarity search on Chroma and return the LLM’s answer plus source IDs.

    Args:
        question: The user’s natural language query.
        chroma_path: Path to the Chroma database directory.

    Returns:
        A tuple of (answer, source_ids).
    """
    
    db = Chroma(
        persist_directory=chroma_path,
        embedding_function=get_embedding_function()
    )
    try:
        #similarity search
        results = db.similarity_search_with_score(question, k=5)

        #filter
        #no explicit filter for demo just keep all results
        filtered_results = results #From my experiments, filter works better with bigger ollama models. 
        #comment out for demonstration and upload since llama3.2 is used.

        #if nothing passes fall back to top 1 so you still get something
        if not filtered_results:
            filtered_results = results[:1]

        #build context string
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
        #prompt and LLM
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
            context=context_text,
            question=question
        )
        response = OllamaLLM(model="llama3.2").invoke(prompt)
        #collect source ids
        sources = [doc.metadata.get("id") for doc, _ in results]
        return response, sources

    finally:
        #no shutdown or close just drop the reference
        del db
