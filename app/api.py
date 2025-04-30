from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .service import RAGService

rag = RAGService()
app = FastAPI(title="RAG‑QA Service", version="0.2")


class QARequest(BaseModel):
    question: str


class QAResponse(BaseModel):
    answer: str
    sources: list[str] | None = None


@app.post("/ask", response_model=QAResponse)
async def ask(req: QARequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="question must be non‑empty")
    return rag.answer(req.question)