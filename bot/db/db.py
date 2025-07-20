# animal-bot/bot.py
# author: kefiiiiir
# version 1.0

import json
import os
from aiogram.types import Message
import aiosqlite

DB_PATH = "database/data.db"

async def initialize_database():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                userId INTEGER,
                chatId INTEGER,
                points INTEGER,
            )
        ''')
        await db.commit()

user_points = {}

async def load_points(user_id: int, chat_id: int):
    """Loads user points to database"""
    global user_points
    if os.path.exists(DB_PATH):
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                cursor = await db.execute(
                    "SELECT points FROM users WHERE userId=? AND chatId=?"
                    , (user_id, chat_id))
                user_points = await cursor.fetchone()
        except:
            user_points = {}

def save_points():
    """Saves user points from user_points dict to json"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
        INSERT INTO users ()'''
                         )
    with open(POINTS_FILE, 'w') as f:
        json.dump(user_points, f)


async def add_points(message: Message):
    user_id = str(message.from_user.id)
    check_user_exists(user_id) 
    user_points[user_id] += 1
    save_points()

async def deduct_points(message: Message, points: int):
    user_id = str(message.from_user.id)
    check_user_exists(user_id) 
    user_points[user_id] -= points
    save_points()

def check_user_exists(user_id: str):
    if not user_id:
        return
    if user_id not in user_points:
        user_points[user_id] = 0