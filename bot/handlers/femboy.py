from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils import utils, r34_api

router = Router()

@router.message(Command("femboy"))
@utils.anti_spam(utils.COMMAND_COOLDOWN)
@utils.check_balance(999)
async def femboy_handler(message: Message):
    """Send random femboy picture"""

    tags = ["femboy", "-video", "-pregnancy", "-ai_generated", "-3d"]
    image = r34_api.get_post(tags)
    # Send image
    await message.answer_photo(image,
                               has_spoiler=True)