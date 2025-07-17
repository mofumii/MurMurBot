# animal-bot/bot.py
# author: Ptmasher
# version 2.1 (VIP and Logging)

import os
from dotenv import load_dotenv
import json
import time
import random
import asyncio
import logging
from functools import wraps
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import r34_api


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),  # Logs in file
        logging.StreamHandler()          # Logs in console
    ]
)
logger = logging.getLogger(__name__)

# Set API token
load_dotenv()
TOKEN = os.getenv("API_TOKEN")
# VIP users are allowed to call some special commands
vip_raw = os.getenv("VIP")
VIP_USERS = json.loads(vip_raw)

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
            logger.info(f"User :{user_id} Call: {handler.__name__}")
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
async def command_duck_handler(message: Message):
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
    await message.answer_photo(photo=image_url)

@dp.message(Command("snake"))
@anti_spam(COMMAND_COOLDOWN)
async def command_snake_handler(message: Message):
    """Send random snake picture"""

    # Get snake picture
    pic_num = random.randint(1, 19)
    pic_path = f"snakes/python{pic_num}.jpg"
    image = FSInputFile(pic_path)
    # Send snake to user
    await message.answer_photo(photo=image,
                               caption="СЛАВА PYTHON БОЖЕ ХРАНИ ПИТОНЧИКОВ")
 
@dp.message(Command("femboy"))
async def command_femboy_handler(message: Message):
    """Send random femboy picture"""

    if not await is_vip(message):
        return
    
    tags = ["femboy", "-video", "-pregnancy", "-ai_generated", "-3d"]
    image = r34_api.get_post(tags)
    # Send image
    await message.answer_photo(image,
                               has_spoiler=True)

@dp.message(Command("r34"))
async def command_r34_handler(message: Message):
    """Send random picture from rule34.xxx"""

    if not await is_vip(message):
        return

    # Example tags
    tags = ["-pregnancy", "-homosexual", "-gay",
            "-ai_generated", "-furry", "-fur",
            "female", "pussy", "-3d"]
    image = r34_api.get_post(tags)
    # Send image
    await message.answer_photo(image,
                               has_spoiler=True)

async def is_vip(message: Message):
    """Checks if user is allowed to use command
        Enabled by default
    """
    uid = message.from_user.id
    vip = str(uid) in VIP_USERS
    logger.info(f"User :{uid} Call:")
    return vip


async def main() -> None:
    """Run bot"""
    print(os.getcwd())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())