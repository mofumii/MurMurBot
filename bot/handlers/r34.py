from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.config import load_env_credentials
from bot.db.db import DatabaseManager

from bot.utils import decorators, r34_api

router = Router()

db = DatabaseManager()

TAGS = load_env_credentials().get("R34_TAGS")

@router.message(Command("r34"))
@decorators.anti_spam(decorators.COMMAND_COOLDOWN)
@decorators.check_balance(500)
async def command_r34_handler(message: Message):
    """Send random picture from rule34.xxx"""

    try:
        image = r34_api.get_post(TAGS)
        await message.answer_photo(image, has_spoiler=True)
        await db.deduct_points(message, 50)
    except Exception:
        await message.reply("Возникла ошибка во время транзакции!")