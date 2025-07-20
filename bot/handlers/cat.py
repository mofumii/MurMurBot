from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils import utils
import time

router = Router()

@router.message(Command("cat"))
@utils.anti_spam(utils.COMMAND_COOLDOWN)
@utils.check_balance(50)
async def command_cat_handler(message: Message):
    """Send random cat picture"""
    
    # Get random cat
    timestamp = int(time.time() * 1000)
    image_url = f"https://cataas.com/cat?timestamp={timestamp}"
    # Send cat picture
    await message.answer_photo(photo=image_url)