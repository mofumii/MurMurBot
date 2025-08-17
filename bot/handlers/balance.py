from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.db.db import DatabaseManager
from bot.utils import decorators

router = Router()
db = DatabaseManager()


@router.message(Command("balance"))
@decorators.anti_spam(decorators.COMMAND_COOLDOWN)
async def command_balance_handler(message: Message):
    """Display user's balance"""

    user_id = message.from_user.id
    chat_id = message.chat.id
    points = await db.get_user_points(user_id, chat_id)
    username = message.from_user.full_name or message.from_user.first_name

    await message.reply(f"📊 у {username} {str(points)} Пойнтсев!")
