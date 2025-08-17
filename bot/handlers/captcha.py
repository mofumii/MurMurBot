from aiogram import F, Router
from aiogram.filters import JOIN_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import (
    CallbackQuery,
    ChatMemberUpdated,
    ChatPermissions,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.bot import bot
from bot.db.db import DatabaseManager

db = DatabaseManager()

router = Router()


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def new_chat_member_handler(update: ChatMemberUpdated):
    new_member = update.new_chat_member.user
    chat_id = update.chat.id

    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=new_member.id,
        permissions=ChatPermissions(can_send_messages=False),
    )

    captcha_button = InlineKeyboardButton(
        text="Я не робот", callback_data=f"not_robot_{new_member.id}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[captcha_button]])

    welcome_message = (
        f"Рады приветствовать в нашем чате, {new_member.full_name}!\n"
        "Для продолжения общения нажми на кнопку ниже"
    )

    gif_url = "https://tenor.com/view/wink-anime-cute-peace-peace-sign-gif-13040107026014624550"

    await bot.send_animation(
        chat_id=chat_id,
        animation=gif_url,
        caption=welcome_message,
        reply_markup=keyboard,
    )


@router.callback_query(F.data.startswith("not_robot"))
async def on_verify(callback: CallbackQuery):
    """
    Allow user to text if they pressed the button
    """
    callback_data = callback.data
    user_id_from_button = int(callback_data.split("_")[2])

    if callback.from_user.id != user_id_from_button:
        await callback.answer("Это не ваша кнопка!", show_alert=True)
        return

    user_id = callback.message.from_user.id
    chat_id = callback.message.chat.id

    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id_from_button,
        permissions=ChatPermissions(can_send_messages=True),
    )

    # Initiate user in database
    db.get_user_points(user_id, chat_id)

    # Delete captcha message
    await bot.delete_message(
        chat_id=callback.message.chat.id, message_id=callback.message.message_id
    )

    await callback.answer("Вход подтвержден. Приятного общения!", show_alert=True)
