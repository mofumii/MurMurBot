# animal-bot/bot/handlers/cat.py
# author: Mofumii
# version 1.0


from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils import decorators
import time

router = Router()

@router.message(Command("cat"))
@decorators.anti_spam(decorators.COMMAND_COOLDOWN)
@decorators.check_balance(50)
async def command_cat_handler(message: Message):
    """Send random cat picture"""
    
    # Get random cat
    timestamp = int(time.time() * 1000)
    image_url = f"https://cataas.com/cat?timestamp={timestamp}"
    # Send cat picture
    await message.answer_photo(photo=image_url)