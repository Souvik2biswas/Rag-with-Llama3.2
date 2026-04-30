FROM python:3.10-slim

# Install curl and other dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set up user and working directory
# Hugging Face Spaces require running as a non-root user
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy requirements and install
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=user . .

# Make start script executable
RUN chmod +x start.sh

# Expose port
EXPOSE 7860

# Start script
ENTRYPOINT ["./start.sh"]
