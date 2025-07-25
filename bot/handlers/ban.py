# animal-bot/bot/handlers/ban.py
# author: Mofumii
# version 1.0


from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.chat_member_status import ChatMemberStatus

router = Router()

@router.message(Command("ban"))
async def ban_handler(message: Message, bot: Bot):
    if message.chat.type == "private":
        await message.reply("Команда /ban не может быть использована в ЛС.")
        return
    
    if message.reply_to_message:
        user_to_ban = message.reply_to_message.from_user
    else:
        await message.reply("Ответьте на сообщения пользователя которого хотите забанить")
        return
    
    try:
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
            await message.reply("У вас нет прав для бана пользователей.")
            return
        
        await bot.ban_chat_member(message.chat.id, user_to_ban.id)
        await message.answer(f"Пользователь {user_to_ban.full_name} забанен.")
    except Exception:
        await message.answer("Ошибка при бане пользователя.")