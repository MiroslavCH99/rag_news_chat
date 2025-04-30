import os

QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY: str | None = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "news_chunks")

EMBEDDING_MODEL_NAME: str = os.getenv(
    "EMB_MODEL", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
)
GEN_MODEL_NAME: str = os.getenv(
    "GEN_MODEL", "TheBloke/Llama-2-13B-chat-GPTQ"
)

TOP_K: int = int(os.getenv("TOP_K", 5))
MAX_ANSWER_TOKENS: int = int(os.getenv("MAX_ANSWER_TOKENS", 256))
DEVICE: int = int(os.getenv("CUDA_DEVICE", 0))  # -1 for CPU
TELEGRAM_BOT_TOKEN: str | None = os.getenv("TELEGRAM_BOT_TOKEN")