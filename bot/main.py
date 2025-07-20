# animal-bot/bot/main.py
# author: Ptmasher
# version 1.0


import asyncio
from bot import bot, dp
from handlers import cat, duck, snake, r34, femboy, balance, message_reward, start
from db import db

async def main():
    dp.include_router(start.router)
    dp.include_router(cat.router)
    dp.include_router(duck.router)
    dp.include_router(snake.router)
    dp.include_router(r34.router)
    dp.include_router(femboy.router)
    dp.include_router(balance.router)
    dp.include_router(message_reward.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    """Run the bot"""
    asyncio.run(db.init_db())
    asyncio.run(main())