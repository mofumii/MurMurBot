from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import Message

from bot.utils import gpt
from bot.utils.decorators import COMMAND_COOLDOWN, anti_spam

router = Router()


@router.message(F.text.lower().startswith("мур"))
@anti_spam(COMMAND_COOLDOWN)
async def chatbot_handler(message: Message):
    user_id = message.from_user.id
    # Remove "мур" from message
    _, user_prompt = message.text.lower().split("мур")
    reply = gpt.get_respond(user_id, user_prompt.strip())
    # Setting parse mode MARKDOWN to display the message correctly
    await message.reply(reply, parse_mode=ParseMode.MARKDOWN)
