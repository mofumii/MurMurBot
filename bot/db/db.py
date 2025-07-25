# animal-bot/db/db.py
# author: Mofumii, kefiiiir
# version 1.1

import os
from aiogram.types import Message
import aiosqlite

DB_PATH = "data.db"

class DatabaseManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
                await db.execute("PRAGMA foreign_keys = ON")

                await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    userId INTEGER,
                    chatId INTEGER,
                    points INTEGER,
                    PRIMARY KEY (userId, chatId)
                )
            ''')
                
                await db.execute('''
                CREATE TABLE IF NOT EXISTS userProfiles (
                    userId INTEGER PRIMARY KEY,
                    os TEXT,
                    specs TEXT,
                    langs TEXT,
                    FOREIGN KEY (userId) REFERENCES users(userId)
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
                        "INSERT OR IGNORE INTO users (userId, chatId, points)" \
                        "VALUES (?, ?, 0)",
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
            
    async def get_user_points(self, message: Message):
        """Returns user's points from balance"""
        user_id = message.from_user.id
        chat_id = message.chat.id

        if os.path.exists(DB_PATH):
            try:
                async with aiosqlite.connect(DB_PATH) as db:
                    await db.execute(
                        "INSERT OR IGNORE INTO users (userId, chatId, points)" \
                        "VALUES (?, ?, 0)",
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

    async def add_points(self, message: Message):
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

    async def deduct_points(self, message: Message, points: int):
        """Adds one point to the user"""
        user_id = message.from_user.id
        chat_id = message.chat.id
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('''
            UPDATE users
            SET points = points - ?
            WHERE userId = ? AND chatId = ? ''',
            (points, user_id, chat_id)
            )
            await db.commit()

    async def create_user(self, uid: int,
                          os: str, specs:str,
                          langs: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
            INSERT INTO userProfiles (userId, os, specs, langs)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(userId) DO UPDATE SET
                os = excluded.os,
                specs = excluded.specs,
                langs = excluded.langs
            ''',
            (uid, os, specs, langs)
            )
            await db.commit()

    async def get_user(self, uid):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
            SELECT os, specs, langs FROM userProfiles WHERE userId=?
            ''',
            (uid,)
            )
            row = await cursor.fetchone()
            return row if row else None
        
    async def user_exists(self, uid):
        """Checks if the user already exist"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                '''SELECT 1 FROM userProfiles WHERE userId=?''',
                (uid,)
                )
            exists = await cursor.fetchone() is not None
            return exists