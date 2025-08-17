import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.db.db import DatabaseManager

from bot.utils import decorators

router = Router()

db = DatabaseManager()

@router.message(Command("cat"))
@decorators.anti_spam(decorators.COMMAND_COOLDOWN)
@decorators.check_balance(50)
async def command_cat_handler(message: Message):
    """Send random cat picture"""

    try:
        # Timestamp for random pic
        timestamp = int(time.time() * 1000)
        image_url = f"https://cataas.com/cat?timestamp={timestamp}"

        await message.answer_photo(photo=image_url)
        await db.deduct_points(message, 50)
    except Exception:
        await message.reply("Возникла ошибка во время транзакции!")
