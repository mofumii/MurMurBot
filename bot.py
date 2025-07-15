# koshka-utka-bot/bot.py
# author: Ptmasher
# version 1.0

import os
from dotenv import load_dotenv
import time
import random
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


# Set API token
load_dotenv()
TOKEN = os.getenv("API_TOKEN")


dp = Dispatcher()
bot = Bot(token=TOKEN)


@dp.message(Command('start'))
async def command_start_handler(message: Message):
    """Display welcome message"""

    await message.answer("""
Привет! Этот бот отправляет случайные фотографии кошек и змей.\n
                         
Список доступный команд:
/duck - фотка случайной утки
/cat - фотка случайной кошки

    """)

@dp.message(Command("duck"))
async def command_snake_handler(message: Message):
    """Send random duck picture"""

    # Get random duck 
    pic_num = random.randint(1, 599)
    image_url = f"https://random-d.uk/api/{pic_num}.jpg"
    # Send duck picture
    await message.answer_photo(photo=image_url)

@dp.message(Command("cat"))
async def command_cat_handler(message: Message):
    """Send random cat picture"""
    
    # Get random cat
    timestamp = int(time.time() * 1000)
    image_url = f"https://cataas.com/cat?timestamp={timestamp}"
    # Send cat picture
    await message.answer_photo(image_url)

async def main() -> None:
    """Run bot"""
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())