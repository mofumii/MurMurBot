# animal-bot/bot/main.py
# author: Mofumii
# version 1.0


import asyncio
from bot import bot, dp
from handlers import *
from db import db
from db.db import DatabaseManager
import logging
import subprocess

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),  # Logs in file
        logging.StreamHandler()          # Logs in console
    ]
)
logger = logging.getLogger(__name__)

db = DatabaseManager()

async def main():
    dp.include_router(ban.router)
    dp.include_router(register.router)
    dp.include_router(start.router)
    dp.include_router(cat.router)
    dp.include_router(stats.router)
    dp.include_router(duck.router)
    dp.include_router(snake.router)
    dp.include_router(r34.router)
    dp.include_router(femboy.router)
    dp.include_router(balance.router)
    dp.include_router(message_reward.router)

    await db.init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    """Run the bot"""
    process = subprocess.Popen(['redis-server'])
    asyncio.run(db.init_db())
    asyncio.run(main())