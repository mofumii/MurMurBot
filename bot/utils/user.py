# animal-bot/bot/utils/user.py
# author: Mofumii
# version 1.1.4

from aiogram import Bot
from aiogram.types import Message, FSInputFile
import logging
import os

logger = logging.getLogger(__name__)

async def get_user_pfp(user_id: int, bot: Bot):
    """
    Retreives the profile picture of the user by their ID.
    """
    try:
        pfps = await bot.get_user_profile_photos(user_id=user_id, limit=1)
        if pfps.total_count > 0:
            user_pfp = pfps.photos[0][-1]
            return user_pfp.file_id
        
        return None
    
    except Exception:
        raise


async def fetch_user_avatar(user_id: int, bot: Bot, message: Message):
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