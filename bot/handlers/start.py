from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils import utils

router = Router()

@router.message(Command("start"))
@utils.anti_spam(utils.COMMAND_COOLDOWN)
async def start_handler(message: Message):
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