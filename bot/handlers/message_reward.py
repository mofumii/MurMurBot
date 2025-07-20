from aiogram import Router
from aiogram.types import Message
from db import db

router = Router()

@router.message()
async def amessage_reward_handler(message: Message):
    """Adds 1 point to the user for a message"""
    await db.add_points(message)