from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

CHROMA_DIR = "./chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MODEL_NAME = "llama3.2"
TOP_K = 3

# ── Prompt Template ───────────────────
RAG_PROMPT = """You are a helpful assistant.
Answer the question using ONLY the provided context.
If the answer is not in the context, say you don't know.

Context: {context}
Question: {question}
Answer:"""

def load_retriever():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    retriever = vector_store.as_retriever(
        search_kwargs={'k': TOP_K}
    )

    return retriever


def format_docs(docs):
    return '\n\n'.join(doc.page_content for doc in docs)


def build_rag_chain(retriever):
    llm = OllamaLLM(model=MODEL_NAME)

    prompt = PromptTemplate.from_template(RAG_PROMPT)

    chain = (
        {
            'context': retriever | format_docs,
            'question': RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


if __name__ == "__main__":
    retriever = load_retriever()
    chain = build_rag_chain(retriever)

    print("RAG Pipeline initialized. Type 'exit' or 'quit' to stop.")
    while True:
        query = input("\nQuestion: ")
        if query.lower() in ["exit", "quit"]:
            break
        print("Thinking...")
        answer = chain.invoke(query)
        print(f"Answer: {answer}")