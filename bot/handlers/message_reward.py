# animal-bot/bot/handlers/message_reward.py
# author: Mofumii, kefiiiir
# version 1.0


from aiogram import Router
from aiogram.types import Message
from db.db import DatabaseManager

router = Router()
db = DatabaseManager()

@router.message()
async def message_reward_handler(message: Message):
    """Adds 1 point to the user for a message"""
    await db.add_points(message)