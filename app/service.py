from __future__ import annotations

from typing import Dict, Any
from .searcher import SemanticSearcher
from .generator import AnswerGenerator


class RAGService:
    def __init__(self) -> None:
        self.searcher = SemanticSearcher()
        self.generator = AnswerGenerator()

    def answer(self, question: str) -> Dict[str, Any]:
        docs = self.searcher.search(question)
        if not docs:
            return {"answer": "Извините, не нашлось информации.", "sources": []}
        answer = self.generator.generate(question, docs)
        return {"answer": answer, "sources": [d["text"] for d in docs]}