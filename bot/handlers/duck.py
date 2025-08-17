import random

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.db.db import DatabaseManager

from bot.utils import decorators

router = Router()

db = DatabaseManager()

@router.message(Command("duck"))
@decorators.anti_spam(decorators.COMMAND_COOLDOWN)
@decorators.check_balance(25)
async def command_duck_handler(message: Message):
    """Send random duck picture"""

    try:
        pic_num = random.randint(1, 599)
        image_url = f"https://random-d.uk/api/{pic_num}.jpg"
        # Send duck picture
        await message.answer_photo(photo=image_url)
        await db.deduct_points(message, 50)
    except Exception:
        await message.reply("Возникла ошибка во время транзакции!")