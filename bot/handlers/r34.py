# animal-bot/bot/handlers/r34.py
# author: Ptmasher
# version 1.0


from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils import decorators
from utils import r34_api

router = Router()

@router.message(Command("r34"))
@decorators.anti_spam(decorators.COMMAND_COOLDOWN)
@decorators.check_balance(500)
async def command_r34_handler(message: Message):
    """Send random picture from rule34.xxx"""

    # Example tags
    tags = ["-pregnancy", "-homosexual", "-gay",
            "-ai_generated", "-furry", "-fur",
            "female", "pussy", "-3d",
            "-futanari"]
    image = r34_api.get_post(tags)
    # Send image
    await message.answer_photo(image,
                               has_spoiler=True)