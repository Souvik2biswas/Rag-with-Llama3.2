from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

DATA_DIR = './data'
CHROMA_DIR = './chroma_db'
EMBED_MODEL = 'all-MiniLM-L6-v2'
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def load_documents(data_dir):
    if not os.path.exists(data_dir):
        print(f"Data directory '{data_dir}' does not exist. Creating it...")
        os.makedirs(data_dir)
        print("Add .pdf files to the ./data folder and run again.")
        exit(1)

    loader = DirectoryLoader(
        data_dir,
        glob='**/*.pdf',        # Changed to PDF
        loader_cls=PyPDFLoader  # Changed to PyPDFLoader
    )
    docs = loader.load()
    return docs

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)
    # Filter out empty chunks and sanitize unicode
    valid_chunks = []
    for c in chunks:
        if c.page_content and c.page_content.strip():
            # Remove lone surrogates that crash the Rust tokenizers
            c.page_content = c.page_content.encode('utf-8', 'replace').decode('utf-8')
            valid_chunks.append(c)
    return valid_chunks

def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL
    )
    vector_store = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    return vector_store

if __name__ == '__main__':
    # Load documents
    docs = load_documents(DATA_DIR)
    print(f"Loaded {len(docs)} pages from PDFs")

    if not docs:
        print("No PDF files found in ./data — add .pdf files and try again.")
        exit(1)

    # Split into chunks
    chunks = split_documents(docs)
    print(f"Created {len(chunks)} chunks")

    if not chunks:
        print("No chunks created — check your PDF files.")
        exit(1)

    # Create vector store
    create_vector_store(chunks)
    print("Ingestion complete. Vector store saved to ./chroma_db")