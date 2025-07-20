# animal-bot/bot/handlers/duck.py
# author: Ptmasher
# version 1.0


from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils import decorators
import random

router = Router()

@router.message(Command("duck"))
@decorators.anti_spam(decorators.COMMAND_COOLDOWN)
@decorators.check_balance(25)
async def command_duck_handler(message: Message):
    """Send random duck picture"""

    # Get random duck 
    pic_num = random.randint(1, 599)
    image_url = f"https://random-d.uk/api/{pic_num}.jpg"
    # Send duck picture
    await message.answer_photo(photo=image_url)