# animal-bot/bot/handlers/femboy.py
# author: Ptmasher
# version 1.0


from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils import decorators
from utils import r34_api

router = Router()

@router.message(Command("femboy"))
@decorators.anti_spam(decorators.COMMAND_COOLDOWN)
@decorators.check_balance(999)
async def femboy_handler(message: Message):
    """Send random femboy picture"""

    tags = ["femboy", "-video", "-pregnancy", "-ai_generated", "-3d"]
    image = r34_api.get_post(tags)
    # Send image
    await message.answer_photo(image,
                               has_spoiler=True)