# Local RAG with Ollama & LangChain

A local, privacy-preserving Retrieval-Augmented Generation (RAG) chatbot application built with Python. It allows you to upload PDF documents and ask questions about them, powered by a local large language model (LLM) via Ollama.

## Features

- **100% Local Processing:** No data leaves your machine. Both document embeddings and LLM inference run locally.
- **PDF Uploads:** Upload multiple PDF documents through the Streamlit interface.
- **Interactive Chat UI:** Built with Streamlit for a seamless conversational experience.
- **Vector Database:** Uses ChromaDB for efficient document retrieval.
- **Docker Support:** Easily deployable via Docker, compatible with Hugging Face Spaces.

## Technology Stack

- **UI Framework:** [Streamlit](https://streamlit.io/)
- **Orchestration:** [LangChain](https://www.langchain.com/)
- **LLM:** [Ollama](https://ollama.com/) (Default: `llama3.2`)
- **Embeddings:** [HuggingFace](https://huggingface.co/) (`all-MiniLM-L6-v2`)
- **Vector Store:** [Chroma](https://www.trychroma.com/)

## Prerequisites

If running natively, ensure you have:
- Python 3.10+
- [Ollama](https://ollama.com/download) installed on your system.

## Setup & Installation

### Option 1: Native Local Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd rag-with-ollama
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Ollama server and pull the model:**
   Make sure the Ollama application is running on your system, then pull the required model:
   ```bash
   ollama pull llama3.2
   ```

5. **Run the Streamlit application:**
   ```bash
   python -m streamlit run app.py
   ```
   Access the web interface at `http://localhost:8501`.

### Option 2: Docker / Hugging Face Spaces

The project includes a `Dockerfile` and `start.sh` script to run everything (including Ollama) in a single container.

1. **Build the Docker image:**
   ```bash
   docker build -t local-rag-app .
   ```

2. **Run the container:**
   ```bash
   docker run -p 7860:7860 local-rag-app
   ```
   Access the web interface at `http://localhost:7860`.

## Project Structure

- `app.py`: The main Streamlit web application. Handles the chat interface, session state, and PDF uploads.
- `ingest.py`: Core logic for loading PDFs, splitting text into chunks, and populating the ChromaDB vector store.
- `rag_pipeline.py`: Configures the LangChain retrieval chain, prompt templates, and Ollama LLM integration.
- `start.sh`: A shell script used in the Docker container to initialize the Ollama server in the background, download the model, and start the Streamlit app.
- `Dockerfile`: Instructions to build the Docker image with all necessary dependencies and run as a non-root user.

## Usage

1. Open the application in your browser.
2. In the sidebar, upload one or more PDF files.
3. Click **Process Documents** and wait for the ingestion process to complete.
4. Once processed, you can start asking questions about the uploaded documents in the chat interface.

## Troubleshooting

- **Connection Error / [WinError 10061]:** Ensure that your Ollama application is running locally before starting the app.
- **Pipeline Not Initialized:** If the pipeline fails to initialize, it might be because the vector store is empty. Make sure to upload and process at least one PDF document first.
