from aiogram import Router
from aiogram.types import Message

from bot.db.db import DatabaseManager

router = Router()
db = DatabaseManager()


@router.message()
async def message_reward_handler(message: Message):
    """Adds 1 point to the user for a message"""
    await db.add_points(message)
