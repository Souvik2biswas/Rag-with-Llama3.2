import streamlit as st
import os
import shutil
from rag_pipeline import load_retriever, build_rag_chain
from ingest import load_documents, split_documents, create_vector_store, DATA_DIR

# Page config
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")

# Initialize session state for chat history and chain
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chain" not in st.session_state:
    st.session_state.chain = None
    try:
        retriever = load_retriever()
        st.session_state.chain = build_rag_chain(retriever)
    except Exception as e:
        # Don't show error immediately on startup if db is just empty
        pass

# Sidebar for document upload
with st.sidebar:
    st.title("📁 Upload PDFs")
    st.markdown("Upload your PDFs")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files", 
        type="pdf", 
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if st.button("Process Documents"):
        if uploaded_files:
            with st.spinner("Processing documents..."):
                try:
                    if not os.path.exists(DATA_DIR):
                        os.makedirs(DATA_DIR)
                    
                    for file in uploaded_files:
                        # Clean filename
                        safe_filename = "".join(c for c in file.name if c.isalnum() or c in " ._-")
                        if not safe_filename.lower().endswith(".pdf"):
                            safe_filename += ".pdf"
                            
                        # Save file
                        file_path = os.path.join(DATA_DIR, safe_filename)
                        with open(file_path, "wb") as f:
                            f.write(file.getbuffer())
                    
                    # Ingest
                    docs = load_documents(DATA_DIR)
                    chunks = split_documents(docs)
                    create_vector_store(chunks)
                    
                    # Reinitialize chain
                    retriever = load_retriever()
                    st.session_state.chain = build_rag_chain(retriever)
                    
                    st.success("Documents processed successfully!")
                except Exception as e:
                    import traceback
                    st.error(f"Error during ingestion: {str(e)}")
                    st.code(traceback.format_exc())
        else:
            st.warning("Please upload at least one PDF.")

# Main chat interface
# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask something..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    with st.chat_message("assistant"):
        if st.session_state.chain is None:
            # Try to initialize one last time
            try:
                retriever = load_retriever()
                st.session_state.chain = build_rag_chain(retriever)
            except Exception:
                pass

        if st.session_state.chain is None:
            response = "Pipeline is not initialized. Please upload a document first."
            st.markdown(response)
        else:
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chain.invoke(prompt)
                    st.markdown(response)
                except Exception as e:
                    response = f"Error: {str(e)}"
                    st.error(response)
        
    # Add to history
    st.session_state.messages.append({"role": "assistant", "content": response})
