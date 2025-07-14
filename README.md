![CI](https://github.com/<YOUR_GITHUB_USERNAME>/LLM-PDF-Analyzer/actions/workflows/ci.yml/badge.svg)

# LLM-PDF-Analyzer

A RAG-powered PDF Q&A web app built with Flask, LangChain, ChromaDB, and Ollama. Upload any PDF, index its contents, then ask natural-language questions—answers show up in seconds, with page-level source tracking.

---

## Features

- **Upload & Index**: Browse or drag-and-drop a PDF; it’s chunked, embedded, and stored in ChromaDB automatically.  
- **Ask Questions**: Enter a query about your PDF and get a concise answer.  
- **Source Tracking**: Every answer lists the page number(s) it came from.  
- **Live Feedback**: A spinner overlay shows progress during indexing and querying.

## Tech Stack

| Layer           | Tool / Library          |
| --------------- | ----------------------- |
| Web framework   | Flask                   |
| RAG pipeline    | LangChain, ChromaDB     |
| Embeddings      | OllamaEmbeddings (Llama3.2) |
| LLM             | OllamaLLM (Llama3.2)    |
| PDF loader      | PyPDF2, langchain-community |

## Prerequisites

- Python 3.8+  
- Git  
- Local Ollama setup with Llama3.2 model  
- (Optional) Docker

## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/<YOUR_GITHUB_USERNAME>/LLM-PDF-Analyzer.git
   cd LLM-PDF-Analyzer

2. Create & activate a venv
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

3. Install dependecies
pip install -r requirements.txt

4. Create a .env file
FLASK_SECRET_KEY=your_secret_key_here

5. Run the app
flask run

Then open http://127.0.0.1:5000 in your browser.

Usage
Click Upload & Index and select a PDF.

Wait for the spinner to finish.

Type your question and hit Ask.

Read the answer and check the “Sources” section for page numbers.

Testing
pytest

We’ve got two simple tests:

test_split_documents.py: verifies that long text chunks correctly split into ≤800-char pieces with metadata preserved.

test_query_rag.py: mocks out Chroma and OllamaLLM to confirm that query_rag() returns the expected answer and source IDs.

Continuous Integration
On every push or PR to main, GitHub Actions will:

Set up Python 3.11

Install your requirements.txt

Run flake8

Check formatting with black --check

Run pytest

See .github/workflows/ci.yml for the full config.

Examples
If you want a quick test PDF, drop it into /examples and then:
cp examples/sample.pdf data/
flask run

Ask something like “What is the effective date of this contract?” and watch the magic.

Contributing
PRs and issues are welcome! Feel free to suggest improvements or new features.

License
MIT © David Shableski
