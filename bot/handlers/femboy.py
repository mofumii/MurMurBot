from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.config import load_env_credentials
from bot.db.db import DatabaseManager

from bot.utils import decorators, r34_api

router = Router()

db = DatabaseManager()

TAGS = load_env_credentials().get("FEMBOY_TAGS")

@router.message(Command("femboy"))
@decorators.anti_spam(decorators.COMMAND_COOLDOWN)
@decorators.check_balance(999)
async def femboy_handler(message: Message):
    """Send random femboy picture"""

    try:
        image = r34_api.get_post(TAGS)
        await message.answer_photo(image, has_spoiler=True)
        await db.deduct_points(message, 50)
    except Exception:
        await message.reply("Возникла ошибка во время транзакции!")