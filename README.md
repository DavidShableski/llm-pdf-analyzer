# LLM-PDF-Analyzer

**LLM-PDF-Analyzer** is a self-hosted web app that lets you upload any PDF, automatically chunk and index its contents in a ChromaDB vector store, then ask natural-language questions against it — all locally, so your documents never leave your machine.

[▶️ Watch the demo video on YouTube](https://www.youtube.com/watch?v=hykruzhymPc)

---

## 🚀 Skills Demonstrated

- **Flask web interface** with secure session management and cookie safety best practices
- **Retrieval-augmented generation (RAG) pipeline** using LangChain, custom PDF loading, text splitting, and metadata-driven chunk-ID generation
- **Integration of ChromaDB with OllamaEmbeddings and OllamaLLM (Llama 3.2)** for on-device embedding and inference
- **Modular Python design** with CLI tooling (`argparse`) and unit tests (`pytest`)
- **CI/CD pipeline with GitHub Actions**: linting (flake8), formatting checks (black), and automated test runs
- **Responsive front end** using semantic HTML, maintainable CSS, and lightweight JavaScript
- **Secrets management** via a `.env` file for development and production readiness

---

## ⚡ Quick Start

1. **Clone the repo**

    ```bash
    git clone https://github.com/DavidShableski/LLM-PDF-Analyzer.git && cd LLM-PDF-Analyzer
    ```

2. **Set up a virtual environment (Python 3.8+)**

    ```bash
    python -m venv venv
    # macOS/Linux
    source venv/bin/activate
    # Windows
    venv\Scripts\activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure your environment**

    Create a `.env` file in the project root:

    ```
    FLASK_SECRET_KEY=your_secure_secret_here
    ```

5. **Run the app**

    ```bash
    flask run
    ```

    Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. Upload a PDF, wait for indexing, then ask your questions.

---

## 🧪 Testing & CI

- **Run tests locally**

    ```bash
    pytest -q
    ```

- **CI pipeline** (defined in `.github/workflows/ci.yml`) automatically:
    - Sets up Python 3.11
    - Installs dependencies
    - Runs `flake8` for linting
    - Checks formatting with `black --check`
    - Executes `pytest`

---

## 📝 License

MIT © David Shableski
