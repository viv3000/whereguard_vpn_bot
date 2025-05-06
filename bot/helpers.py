import qrcode
from typing import Optional
from aiogram import Bot
from aiogram.types import User

from bot.VPNBot import VPNBot
from bot.keyboards import main_menu_keyboard, start_keyboard
from services.entities import UserBuilder


async def send_message_to_support(text: str, user: User, bot: VPNBot):
    if (user.username == None):
        await bot.send_message(chat_id=bot.support_chat_id, text=f"tg://openmessage?user_id={user.id} вопрошает:\n{text}")
    else:
        await bot.send_message(chat_id=bot.support_chat_id, text=f"@{user.username} вопрошает:\n{text}")


async def send_message_to_log(message_text, user: User, bot: VPNBot):
    if (user.username == None):
        await bot.send_message(chat_id=bot.support_chat_id, text=f"{message_text}\ntg://openmessage?user_id={user.id}")
    else:
        await bot.send_message(chat_id=bot.support_chat_id, text=f"{message_text}\n@{user.username}")


def create_qr(text):
    return qrcode.make(text).get_image()

async def await_with_markup(message, text, text_false, tg_user: User, messages):
    builder = UserBuilder(tg_user)
    user = builder.build()
    if user.is_payed():
        await message.answer(text, reply_markup=main_menu_keyboard(messages))
    else:
        await message.answer(text_false, reply_markup=start_keyboard(messages))


async def await_with_markup_file(answer, file, tg_user: User, messages):
    builder = UserBuilder(tg_user)
    user = builder.build()
    if user.is_payed():
        await answer(file, reply_markup=main_menu_keyboard(messages))
    else:
        await answer(file, reply_markup=start_keyboard(messages))
