import io
import random
from PIL import Image

from aiogram import Bot
from aiogram.types import BufferedInputFile, CallbackQuery, Message, User
from services.entities import UserBuilder
from services.data import Data

from bot.helpers import create_qr
from bot.keyboards import start_keyboard, main_menu_keyboard
 

async def start(message: Message, tg_user: User):
    if message.from_user:
        builder = UserBuilder(tg_user)
        user = builder.build()
        if user.is_payed():
            await message.answer("Привет!", reply_markup=main_menu_keyboard)
    else:
        await message.answer("Привет! Этот бот предназначен для покупки VPN", reply_markup=start_keyboard)


async def get_config(message: Message, tg_user: User):
    await message.answer("Установи приложение wireguard\n <a href='https://play.google.com/store/apps/details?id=com.wireguard.android&hl=ru'>windows</a>\n<a href='https://play.google.com/store/apps/details?id=com.wireguard.android'>android</a>\n<a href='https://apps.apple.com/ru/app/wireguard/id1441195209'>ios</a>\n<a href='https://www.wireguard.com/install/'>остальное</a>")
    builder = UserBuilder(tg_user)
    user = builder.build()
    print(user.user_data.id)
    config = user.get_config()

    text = Data.compile_config_file(config.id)
    text_file = BufferedInputFile(text.encode(), filename="conf.conf")

    byte_qr = io.BytesIO()
    create_qr(text).save(byte_qr, "png")
    byte_qr.seek(0)
    photo_file = BufferedInputFile(byte_qr.read(), filename="qr.png")

    await message.answer(text)
    await message.answer_document(text_file)
    await message.answer_photo(photo_file)

