# animal-bot/bot/handlers/register.py
# author: Mofumii
# version 1.0

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging
from utils.decorators import anti_spam, COMMAND_COOLDOWN
from db.db import DatabaseManager
import redis


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),  # Logs in file
        logging.StreamHandler()          # Logs in console
    ]
)
logger = logging.getLogger(__name__)

pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0
)
user_data_cache = redis.Redis(connection_pool=pool)
REGISTRATION_TTL = 1800

db = DatabaseManager()

class RegistrationStates(StatesGroup):
    waiting_for_os = State()
    waiting_for_specs = State()
    waiting_for_langs = State()
    waiting_pfp = State()

class ConfirmRegistration(StatesGroup):
    registration_confirm = State()

router = Router()

# Тут будет регистрация и будет сохранены ОС юзера, специализация, языки, хз еще чота
# Короч тут просто повторяется одно и тож в каждой функцие


@router.message(Command("register"))
@anti_spam(COMMAND_COOLDOWN)
async def register_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if not message.chat.type == 'private':
        await message.reply("регистрация должна проходить в ЛС с ботом!")
        return
    
    if await db.user_exists(user_id):
        await message.reply("Ваш профиль уже заполнен. Хотите заполнить заново? (Y/N)")
        await state.set_state(ConfirmRegistration.registration_confirm)
        return
    
    await start_registration(message, state)

@router.message(ConfirmRegistration.registration_confirm)
async def registration_confirm(message: Message, state: FSMContext):
    user_answer = message.text.strip().lower()
    await state.clear()
    
    if user_answer == "y":
        await start_registration(message, state)
    else:
        await message.reply("Регистрация отменена.")

async def start_registration(message: Message, state: FSMContext):
    text = (
    "Отлично! Давайте приступим к ргеистрации.\n"
    "Регистрация состоит из трёх пунктов и требует всего минуту времени.\n\n"
    "Введите вашу операционную систему."
    )
    await message.reply(text)
    await state.set_state(RegistrationStates.waiting_for_os)

@router.message(RegistrationStates.waiting_for_os)
async def add_user_specs(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_os = message.text.strip()

    try:
        user_data_cache.setex(f"registration:{user_id}:os",
                              REGISTRATION_TTL, user_os)
    except redis.RedisError as e:
        await message.answer("Произошла ошибка при сохранеинии данных. Попробуйте позже")
        logger.error(f"Can't save: {e}")
        return
    
    await state.clear()
    await message.answer("Введите ваши навыки/спецификацию")
    await state.set_state(RegistrationStates.waiting_for_specs)

@router.message(RegistrationStates.waiting_for_specs)
async def add_user_langs(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_specs = message.text.strip()

    try:
        user_data_cache.setex(f"registration:{user_id}:specs",
                              REGISTRATION_TTL, user_specs)
    except redis.RedisError as e:
        await message.answer("Произошла ошибка при сохранении данных. Попробуйте позже.")
        logger.error(f"Can't save: {e}")
        return
    
    await state.clear()
    await message.answer("Введите ваши языки програмирования")
    await state.set_state(RegistrationStates.waiting_for_langs)

@router.message(RegistrationStates.waiting_for_langs)
async def add_user_pfp(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    user_langs = message.text.strip()

    try:
        user_data_cache.setex(f"registration:{user_id}:langs",
                              REGISTRATION_TTL, user_langs)
    except redis.RedisError as e:
        await message.answer("Произошла ошибка при сохранении данных. Попробуйте позже.")
        logger.error(f"Can't save: {e}")
        return
    
    succeess_message = (
        "Регистрация успешно завершена!\n\n"
        "Вы можете посмотреть свой профиль используя /stats\n"
        ""
    )
    await dump_to_db(user_id)
    await state.clear()
    await message.answer("Регистрация завершена!")

async def dump_to_db(user_id):
    try:
        os = user_data_cache.get(f"registration:{user_id}:os")
        specs = user_data_cache.get(f"registration:{user_id}:specs")
        langs = user_data_cache.get(f"registration:{user_id}:langs")

        os = os.decode() if isinstance(os, bytes) else os
        specs = specs.decode() if isinstance(specs, bytes) else specs
        langs = langs.decode() if isinstance(langs, bytes) else langs

        await db.create_user(user_id, os=os, specs=specs, langs=langs)

        user_data_cache.delete(f"registration:{user_id}:os")
        user_data_cache.delete(f"registration:{user_id}:specs")
        user_data_cache.delete(f"registration:{user_id}:langs")

    except redis.RedisError:
        logger.error(f"Can't save: {e}")
        raise
    except Exception as e:
        logger.error(f"Can't save: {e}")
        raise