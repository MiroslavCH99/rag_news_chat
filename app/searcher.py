from __future__ import annotations

from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from . import config


class SemanticSearcher:
    def __init__(self) -> None:
        self.embedder = SentenceTransformer(
            config.EMBEDDING_MODEL_NAME,
            device=f"cuda:{config.DEVICE}" if config.DEVICE >= 0 else "cpu",
        )
        self.qdrant = QdrantClient(url=config.QDRANT_URL, api_key=config.QDRANT_API_KEY)

    def search(self, query: str, top_k: int | None = None) -> List[Dict[str, Any]]:
        if top_k is None:
            top_k = config.TOP_K
        vector = self.embedder.encode(query, convert_to_numpy=True).tolist()
        hits = self.qdrant.search(
            collection_name=config.QDRANT_COLLECTION,
            query_vector=vector,
            limit=top_k,
            with_payload=True,
        )
        return [
            {
                "text": h.payload.get("text", ""),
                "source": h.payload.get("source"),
                "score": h.score,
            }
            for h in hits
        ]