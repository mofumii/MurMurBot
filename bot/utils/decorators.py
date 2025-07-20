# animal-bot/bot/utils/decorators.py
# author: Ptmasher
# version 1.0


from aiogram.types import Message
from functools import wraps
import time
from db import db


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
            
            points = await db.get_user_points(message)
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
            user_id = get_user_id(message)
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

def get_user_id(message: Message) -> str | None:
    if message.from_user:
        return str(message.from_user.id)
    return None