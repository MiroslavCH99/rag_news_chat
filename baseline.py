import os
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Импорт классов из langchain
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# Pydantic-модель для входящего запроса
class QueryRequest(BaseModel):
    question: str

app = FastAPI()

# Глобальная переменная для хранения QA-цепочки
qa_chain = None

def load_csv_documents(csv_file: str):
    """
    Загружает данные из CSV-файла и преобразует каждую строку в объект Document.
    Текст документа формируется как объединение заголовка, даты, времени, темы, URL и основного контента.
    Метаданные сохраняются для возможности дальнейшей фильтрации и цитирования.
    """
    df = pd.read_csv(csv_file)
    documents = []
    for _, row in df.iterrows():
        # Собираем текст с указанием ключевых метаданных
        doc_text = (
            f"Заголовок: {row['title']}\n"
            f"Дата: {row['date']} {row['time']}\n"
            f"Тема: {row['topic']}\n"
            f"URL: {row['url']}\n\n"
            f"{row['content']}"
        )
        # Можно сохранить и другие метаданные для дальнейшей обработки
        metadata = {
            "id": row["id"],
            "date": row["date"],
            "time": row["time"],
            "title": row["title"],
            "topic": row["topic"],
            "url": row["url"]
        }
        documents.append(Document(page_content=doc_text, metadata=metadata))
    return documents

@app.on_event("startup")
async def startup_event():
    csv_file = os.path.join("news_data", "news.csv")
    if not os.path.exists(csv_file):
        print(f"CSV файл {csv_file} не найден. Убедитесь, что файл существует и доступен.")
        return

    documents = load_csv_documents(csv_file)

    # 2. Разбиение документов на фрагменты для улучшения качества поиска
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    split_docs = text_splitter.split_documents(documents)

    # 3. Инициализация модели эмбеддингов (используется модель SentenceTransformers)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    # 4. Построение векторного хранилища с использованием FAISS
    vector_store = FAISS.from_documents(split_docs, embeddings)

    # 5. Инициализация LLM – используется OpenAI GPT‑3.5‑turbo с температурой 0 для детерминированных ответов
    llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # 6. Создание RetrievalQA цепочки с выдачей топ-3 найденных фрагментов
    global qa_chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3})
    )
    print("QA chain успешно инициализирована")

@app.post("/query")
async def query(request: QueryRequest):
    if qa_chain is None:
        return {"error": "Система еще не готова. Попробуйте позже."}
    answer = qa_chain.run(request.question)
    return {"answer": answer}

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
