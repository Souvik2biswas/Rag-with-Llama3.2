#!/bin/bash

# Start Ollama server in the background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama server to be ready
echo "Waiting for Ollama to start..."
until curl -s http://localhost:11434/api/tags > /dev/null; do
    sleep 2
done
echo "Ollama is running!"

# Pull the required model
echo "Pulling llama3.2 model..."
ollama pull llama3.2

# Start the Streamlit app
echo "Starting Streamlit app..."
python -m streamlit run app.py --server.port 7860 --server.address 0.0.0.0
