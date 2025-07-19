# animal-bot/bot.py
# author: mofumii, kefiiiiir
# version 3.0 (POINTS SYSTEM!!!)

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
import db


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

def check_balance(required_points: int):
    def decorator(handler):
        @wraps(handler)
        async def wrapper(message: Message, *args, **kwargs):
            user_id = get_user_id(message)
            if not user_id:
                await message.reply("❌ Could not identify user.")
                return
            
            logger.info(f"User: {user_id} called: {handler.__name__}")
            
            points = db.user_points[user_id]
            if points < required_points:
                await message.reply(
                    f"❌ Недостаточно поинтов."
                    f"Ваш баланс: {points} поинтов."
                    f"Необходимо поинтов: {required_points}")
                return
            
            await db.deduct_points(message, required_points)
            return await handler(message, *args, **kwargs)
        return wrapper
    return decorator

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
Привет! Этот бот отправляет случайные фотографии зверей за баллы.\n
Один бал начисляется за каждое сообщение в чате (Добавь бота в групчат)\n
                         
Список доступный команд:
/duck - фотка случайной утки
/cat - фотка случайной кошки
/snake - фотка питончика
/balance - проверить баланс
    """)

@dp.message(Command("duck"))
@anti_spam(COMMAND_COOLDOWN)
@check_balance(25)
async def command_duck_handler(message: Message):
    """Send random duck picture"""

    # Get random duck 
    pic_num = random.randint(1, 599)
    image_url = f"https://random-d.uk/api/{pic_num}.jpg"
    # Send duck picture
    await message.answer_photo(photo=image_url)

@dp.message(Command("cat"))
@anti_spam(COMMAND_COOLDOWN)
@check_balance(50)
async def command_cat_handler(message: Message):
    """Send random cat picture"""
    
    # Get random cat
    timestamp = int(time.time() * 1000)
    image_url = f"https://cataas.com/cat?timestamp={timestamp}"
    # Send cat picture
    await message.answer_photo(photo=image_url)

@dp.message(Command("snake"))
@check_balance(50)
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
@check_balance(999)
async def command_femboy_handler(message: Message):
    """Send random femboy picture"""

    tags = ["femboy", "-video", "-pregnancy", "-ai_generated", "-3d"]
    image = r34_api.get_post(tags)
    # Send image
    await message.answer_photo(image,
                               has_spoiler=True)

@dp.message(Command("r34"))
@check_balance(500)
async def command_r34_handler(message: Message):
    """Send random picture from rule34.xxx"""

    # Example tags
    tags = ["-pregnancy", "-homosexual", "-gay",
            "-ai_generated", "-furry", "-fur",
            "female", "pussy", "-3d"]
    image = r34_api.get_post(tags)
    # Send image
    await message.answer_photo(image,
                               has_spoiler=True)

@dp.message(Command("balance"))
@anti_spam(10)
async def command_balance_handler(message: Message):
    """Display user nalance"""
    user_id = get_user_id(message)
    if not user_id:
        await message.reply("❌ Could not identify user.")
        return
    
    points = db.user_points[user_id]
    username = message.from_user.full_name or message.from_user.first_name
    
    await message.reply(
        f"📊 у {username} {points} Пойнтсев!"
    )

@dp.message()
async def add_points(message: Message):
    """Adds 1 point to the user for a message"""
    await db.add_points(message)

def get_user_id(message: Message) -> str | None:
    if message.from_user:
        return str(message.from_user.id)
    return None

async def main() -> None:
    """Run bot"""
    db.load_points()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
