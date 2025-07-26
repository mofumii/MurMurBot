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