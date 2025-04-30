import asyncio
import logging
from typing import Any

import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from app import config

logger = logging.getLogger(__name__)
API_URL = "http://localhost:8000/ask"  # same container network


def run_bot():
    if not config.TELEGRAM_BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN not set; bot disabled")
        return

    bot = Bot(config.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(bot)
    client = httpx.AsyncClient()

    @dp.message_handler()
    async def handle_msg(msg: types.Message):
        q = msg.text or ""
        if not q.strip():
            await msg.reply("Пришлите текстовый вопрос.")
            return
        await msg.chat.do("typing")
        try:
            r: Any = await client.post(API_URL, json={"question": q})
            data = r.json()
            await msg.reply(data.get("answer", "Ошибка"))
        except Exception as e:  # noqa: BLE001
            logger.exception(e)
            await msg.reply("Произошла ошибка на сервере.")

    executor.start_polling(dp, skip_updates=True)