FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy .env file into the container
COPY .env .env

# Copy project source code (backend, frontend, app)
COPY backend/ /app/backend
COPY frontend/ /app/frontend
COPY app/ /app/app

# Use /tmp for Streamlit config/cache/runtime (writable in Hugging Face)
ENV STREAMLIT_RUNTIME_DIR=/tmp/.streamlit
ENV STREAMLIT_CACHE_DIR=/tmp/.streamlit-cache
ENV STREAMLIT_BROWSER_GATHERUSAGESTATS=false
ENV PYTHONPATH=/app
ENV HOME=/tmp

# Expose ports
EXPOSE 8000
EXPOSE 7860

# Start FastAPI (background) + Streamlit (main process)
CMD ["bash", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & exec streamlit run frontend/main.py --server.address=0.0.0.0 --server.port=7860"]
