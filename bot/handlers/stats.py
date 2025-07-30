# animal-bot/bot/handlers/stats.py
# author: Mofumii
# version 1.1.4

from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile
import os
from aiogram.filters import Command
import logging
from utils import motivation
from utils.user import get_user_pfp
from utils.decorators import anti_spam, COMMAND_COOLDOWN
from db.db import DatabaseManager

logger = logging.getLogger(__name__)

db = DatabaseManager()

router = Router()

@router.message(Command("stats"))
@anti_spam(COMMAND_COOLDOWN)
async def stats_handler(message: Message, bot: Bot):

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.from_user.id
    
    user_data = await db.get_user(user_id)

    if not user_data:
        await message.reply(
        "Пользователь еще не зарегестрирован. " \
        "Регистрация доступна в ЛС с ботом"
        )
        return
    
    try:
        pfp = await get_user_pfp(user_id, bot)
    except Exception:
        await message.reply("Произошла ошибка при получении аватарки пользователя.")
        return
    
    if not pfp:
        blank_pfp_path = "blank-pfp.jpg"
        if not os.path.exists(blank_pfp_path):
            await message.reply("Невозможно загрузить фотографию профиля.")
            return
        
        try:    
            pfp = FSInputFile(blank_pfp_path)
        except Exception:
            await message.reply("Возникла непредвиденная ошибка. Повторите запрос позже.")
            return

    if not pfp:
        return

    user = await bot.get_chat(user_id)
    user_name = user.full_name
    user_points = await db.get_user_points(message)
    motivational_phrase = motivation.get_random_phrase(user_name)

    caption = (
        f"<b>🌸 {user_name} 🌸</b>\n\n"
        f"°❀⋆.ೃ࿔*:･☆°❀⋆.ೃ࿔*:･\n\n"
        f"🐱 ОС: {user_data[0]}\n"
        f"🌟 Навыки: {user_data[1]}\n"
        f"📖 Языки: {user_data[2]}\n"
        f"🍬 Поинты: {user_points}\n\n"
        f"<i>{motivational_phrase}! 🌟</i>"
    )

    if user_name and user_points is not None and motivational_phrase and user_data:
        await message.answer_photo(pfp, caption=caption)
    else:
        await message.reply("Произошла ошибка с нашей стороны. Повторите позже!")