# animal-bot/bot/handlers/chatbot.py
# author: Mofumii
# version 1.0


from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from utils import gpt
from utils.decorators import anti_spam, COMMAND_COOLDOWN

router = Router()

@router.message(F.text.lower().startswith("мур"))
@anti_spam(COMMAND_COOLDOWN)
async def chatbot_handler(message: Message):
    user_id = message.from_user.id
    # Remove "мур" from message
    _, user_prompt = message.text.lower().split("мур")
    reply = gpt.get_answer(user_id, user_prompt.strip())
    # Setting parse mode MARKDOWN to display the message correctly
    await message.reply(reply, parse_mode=ParseMode.MARKDOWN)
