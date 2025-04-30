# Новостной чат-бот
Позволяет получать актуальную информацию из новстных источников.
- Главные источники на данный момент: Interfax

# Структура сервиса

```
# ├── app/
# │   ├── __init__.py
# │   ├── config.py          # конфиг проекта
# │   ├── searcher.py        # retrieval
# │   ├── generator.py       # LLaMA‑chat
# │   ├── service.py         # RAG pipeline
# │   └── api.py             # FastAPI
# ├── bot/
# │   ├── __init__.py
# │   └── telegram_bot.py    # aiogram bot
# ├── main.py                # launch API & bot concurrently
# ├── requirements.txt       # pip deps
# └── Dockerfile             # production image
```
# Описание FASTAPI эндпоинта
POST /ask (JSON {question} → {answer, sources}).
