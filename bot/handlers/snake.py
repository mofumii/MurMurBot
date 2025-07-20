# animal-bot/bot/handlers/snake.py
# author: Ptmasher
# version 1.0


from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from utils import decorators
import random

router = Router()

@router.message(Command("snake"))
@decorators.anti_spam(decorators.COMMAND_COOLDOWN)
@decorators.check_balance(50)
async def command_snake_handler(message: Message):
    """Send random snake picture"""

    # Get snake picture
    pic_num = random.randint(1, 19)
    pic_path = f"snakes/python{pic_num}.jpg"
    image = FSInputFile(pic_path)
    # Send snake to user
    await message.answer_photo(photo=image,
                            caption="СЛАВА PYTHON БОЖЕ ХРАНИ ПИТОНЧИКОВ")