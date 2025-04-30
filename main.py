import asyncio
import logging
import uvicorn
from bot.telegram_bot import run_bot
from app.api import app

logging.basicConfig(level=logging.INFO)


async def start_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio.gather(start_api(), asyncio.to_thread(run_bot))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass