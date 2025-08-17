import asyncio
import logging

from bot.bot import bot, dp
from bot.db.db import DatabaseManager
from bot.handlers import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

db = DatabaseManager()


async def main():
    dp.include_router(chatbot.router)
    dp.include_router(captcha.router)
    dp.include_router(ban.router)
    dp.include_router(register.router)
    dp.include_router(start.router)
    dp.include_router(cat.router)
    dp.include_router(stats.router)
    dp.include_router(duck.router)
    dp.include_router(r34.router)
    dp.include_router(femboy.router)
    dp.include_router(balance.router)
    dp.include_router(message_reward.router)

    await db.init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=None)


if __name__ == "__main__":
    asyncio.run(db.init_db())
    asyncio.run(main())
