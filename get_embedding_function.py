from langchain_ollama import OllamaEmbeddings

def get_embedding_function() -> OllamaEmbeddings:
    """
    Return an OllamaEmbeddings instance configured for Llama 3.2.
    """
    return OllamaEmbeddings(model="llama3.2")