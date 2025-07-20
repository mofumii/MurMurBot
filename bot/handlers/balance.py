from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils import utils
from db import db

router = Router()

@router.message(Command("balance"))
@utils.anti_spam(utils.COMMAND_COOLDOWN)
async def command_balance_handler(message: Message):
    """Display user nalance"""
    user_id = utils.get_user_id(message)
    if not user_id:
        await message.reply("❌ Could not identify user.")
        return
    
    points = db.user_points[user_id]
    username = message.from_user.full_name or message.from_user.first_name
    
    await message.reply(
        f"📊 у {username} {points} Пойнтсев!"
    )