from ingest import load_documents, split_documents, DATA_DIR, EMBED_MODEL
from langchain_huggingface import HuggingFaceEmbeddings

docs = load_documents(DATA_DIR)
chunks = split_documents(docs)
texts = [c.page_content for c in chunks]

embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

for i, t in enumerate(texts):
    try:
        embeddings.embed_documents([t])
    except Exception as e:
        print(f"Failed at index {i}!")
        print(f"Type: {type(t)}")
        with open("failed_text.txt", "w", encoding="utf-8") as f:
            f.write(t)
        break
