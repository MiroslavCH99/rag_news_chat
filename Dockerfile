FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy source
COPY . .

# default env (override at runtime)
ENV QDRANT_URL=http://qdrant:6333 \
    QDRANT_COLLECTION=news_chunks \
    EMB_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2 \
    GEN_MODEL=TheBloke/Llama-2-13B-chat-GPTQ \
    CUDA_DEVICE=0

EXPOSE 8000

CMD ["python", "main.py"]