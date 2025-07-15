# animal-bot/bot.py
# author: Ptmasher
# version 1.0

import os
from dotenv import load_dotenv
import time
import random
import asyncio
from functools import wraps
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile


# Set API token
load_dotenv()
TOKEN = os.getenv("API_TOKEN")


dp = Dispatcher()
bot = Bot(token=TOKEN)

COMMAND_COOLDOWN = 10

# Users waiting for cooldown
user_cooldowns = {}

def anti_spam(delay: int):
    """Sets cooldown for commands for a user"""
    def decorator(handler):
        @wraps(handler)
        async def wrapper(message: Message, *args, **kwargs):
            user_id = message.from_user.id
            now = time.time()

            # Check if user is on cooldown
            last_call = user_cooldowns.get((handler.__name__, user_id), 0)
            if now - last_call < delay:
                # Send remaining time
                remaining = int(delay - (now - last_call))
                await message.reply(f"Подожди {remaining} секунд перед повтором.")
                return
            
            # Save current time as last call time
            user_cooldowns[(handler.__name__), user_id] = now
            return await handler(message, *args, **kwargs)
        return wrapper
    return decorator

@dp.message(Command('start'))
async def command_start_handler(message: Message):
    """Display welcome message"""

    await message.answer("""
Привет! Этот бот отправляет случайные фотографии кошек, змей и уток.\n
                         
Список доступный команд:
/duck - фотка случайной утки
/cat - фотка случайной кошки
/snake - фотка питончика
    """)

@dp.message(Command("duck"))
@anti_spam(COMMAND_COOLDOWN)
async def command_snake_handler(message: Message):
    """Send random duck picture"""

    # Get random duck 
    pic_num = random.randint(1, 599)
    image_url = f"https://random-d.uk/api/{pic_num}.jpg"
    # Send duck picture
    await message.answer_photo(photo=image_url)

@dp.message(Command("cat"))
@anti_spam(COMMAND_COOLDOWN)
async def command_cat_handler(message: Message):
    """Send random cat picture"""
    
    # Get random cat
    timestamp = int(time.time() * 1000)
    image_url = f"https://cataas.com/cat?timestamp={timestamp}"
    # Send cat picture
    await message.answer_photo(image_url)

@dp.message(Command("snake"))
@anti_spam(COMMAND_COOLDOWN)
async def command_snake_handler(message: Message):
    """Send random snake picture"""

    # Get snake picture
    pic_num = random.randint(1, 61)
    pic_path = f"snakes/python{pic_num}.jpg"
    photo = FSInputFile(pic_path)
    # Send snake to user
    await message.answer_photo(photo=photo, caption="СЛАВА PYTHON БОЖЕ ХРАНИ ПИТОНЧИКОВ")
 
async def main() -> None:
    """Run bot"""
    print(os.getcwd())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())