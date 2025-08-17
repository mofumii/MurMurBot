import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot.db.db import DatabaseManager
from bot.utils.decorators import COMMAND_COOLDOWN, anti_spam

logger = logging.getLogger(__name__)

user_data_cache = {}

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

    if not message.chat.type == "private":
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
async def ask_user_specs(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_os = message.text.strip()

    try:
        user_data_cache[f"registration:{user_id}:os"] = user_os
    except Exception as e:
        await message.answer("Произошла ошибка при сохранении данных. Попробуйте позже")
        logger.error(f"Unable to save user os: {e}")
        return

    await state.clear()
    await message.answer("Введите ваши навыки/спецификацию")
    await state.set_state(RegistrationStates.waiting_for_specs)


@router.message(RegistrationStates.waiting_for_specs)
async def ask_user_langs(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_specs = message.text.strip()

    try:
        user_data_cache[f"registration:{user_id}:specs"] = user_specs
    except Exception as e:
        await message.answer(
            "Произошла ошибка при сохранении данных. Попробуйте позже."
        )
        logger.error(f"Unable to save user specs: {e}")
        return

    await state.clear()
    await message.answer("Введите ваши языки програмирования")
    await state.set_state(RegistrationStates.waiting_for_langs)


@router.message(RegistrationStates.waiting_for_langs)
async def ask_user_pfp(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_langs = message.text.strip()

    try:
        user_data_cache[f"registration:{user_id}:langs"] = user_langs
    except Exception as e:
        await message.answer(
            "Произошла ошибка при сохранении данных. Попробуйте позже."
        )
        logger.error(f"Unable to save user languages: {e}")
        return

    success_message = (
        "Регистрация успешно завершена!\n\n"
        "Вы можете посмотреть свой профиль используя /stats"
        ""
    )
    await dump_to_db(message)
    await state.clear()
    await message.answer(success_message)


async def dump_to_db(message: Message):
    user_id = message.from_user.id
    try:
        os = user_data_cache.pop(f"registration:{user_id}:os")
        specs = user_data_cache.pop(f"registration:{user_id}:specs")
        langs = user_data_cache.pop(f"registration:{user_id}:langs")

        await db.create_user(user_id, os=os, specs=specs, langs=langs)

    except Exception as e:
        await message.answer(
            "Произошла ошибка при сохранении данных. Попробуйте позже."
        )
        logger.error(f"Unable to save user information to the database: {e}")
        raise
