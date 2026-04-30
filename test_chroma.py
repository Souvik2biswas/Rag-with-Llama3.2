from ingest import load_documents, split_documents, DATA_DIR, EMBED_MODEL
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

docs = load_documents(DATA_DIR)
chunks = split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

try:
    vector_store = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory="./test_chroma_db"
    )
    print("Success!")
except Exception as e:
    print("Failed!")
    import traceback
    traceback.print_exc()
