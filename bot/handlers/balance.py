# animal-bot/bot/handlers/balance.py
# author: Mofumii, kefiiiir
# version 1.0


from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils import decorators
from db.db import DatabaseManager

router = Router()
db = DatabaseManager()

@router.message(Command("balance"))
@decorators.anti_spam(decorators.COMMAND_COOLDOWN)
async def command_balance_handler(message: Message):
    """Display user's balance"""

    points = await db.get_user_points(message=message)
    username = message.from_user.full_name or message.from_user.first_name
    
    await message.reply(
        f"📊 у {username} {str(points)} Пойнтсев!"
    )