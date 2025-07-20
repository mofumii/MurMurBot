# animal-bot/bot/db/db.py
# author: kefiiiiir
# version 1.0


import os
from aiogram.types import Message
import aiosqlite

DB_PATH = "data.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                userId INTEGER,
                chatId INTEGER,
                points INTEGER,
                PRIMARY KEY (userId, chatId)
            )
        ''')
        await db.commit()

async def get_user_points(message: Message):
    """Returns user's points from balance"""
    user_id = message.from_user.id
    chat_id = message.chat.id

    if os.path.exists(DB_PATH):
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute(
                    "INSERT OR IGNORE INTO users (userId, chatId, points) VALUES (?, ?, 0)",
                    (user_id, chat_id)
                )

                await db.commit()

                cursor = await db.execute(
                    "SELECT points FROM users WHERE userId=? AND chatId=?"
                    , (user_id, chat_id))
                row = await cursor.fetchone()
                if row is not None:
                    return row[0]
                else:
                    return 0
        except Exception:
            return
            
async def add_points(message: Message):
    """Adds one point to the user"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
        UPDATE users
        SET points = points + 1
        WHERE userId = ? AND chatId = ? ''',
        (user_id, chat_id)
        )
        await db.commit()

async def deduct_points(message: Message, points):
    user_id = message.from_user.id
    chat_id = message.chat.id
    """Deducts points from the user"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
        UPDATE users
        SET points = points - ?
        WHERE userId = ? AND chatId = ? ''',
        (points, user_id, chat_id)
        )
        await db.commit()