import datetime
import io

from aiogram.types import BufferedInputFile, Message, User
from bot.VPNBot import VPNBot
from services.entities import UserBuilder
from services.data import Data

from bot.helpers import await_with_markup, await_with_markup_file, create_qr
from bot.keyboards import start_keyboard, main_menu_keyboard
 

async def start(message: Message, tg_user: User, messages):
    await await_with_markup(
        message, 
        messages["greetings"], messages["greetings_first"], 
        tg_user, 
        messages
    )


async def get_config(message: Message, tg_user: User, messages):
    builder = UserBuilder(tg_user)
    user = builder.build()

    config = user.get_config()

    text = Data.compile_config_file(config.id)
    text_file = BufferedInputFile(text.encode(), filename="conf.conf")

    byte_qr = io.BytesIO()
    create_qr(text).save(byte_qr, "png")
    byte_qr.seek(0)
    photo_file = BufferedInputFile(byte_qr.read(), filename="qr.png")

    await await_with_markup_file(
        message.answer_document, 
        text_file, 
        tg_user, 
        messages
    )
    await await_with_markup_file(
        message.answer_photo, 
        photo_file, 
        tg_user, 
        messages
    )


async def get_date(message: Message, tg_user: User, messages):
    builder = UserBuilder(tg_user)
    user = builder.build()
    date = user.get_expiration_date()
    if (date>datetime.datetime.today().date()):
        date_format = str(date.strftime("%Y.%m.%d"))
        await message.answer(messages["get_date"].replace("<date>", date_format))
    else:
        await message.answer(messages["is_not_payd"])


async def get_instruction(message: Message, messages):
    await message.answer(messages["instruction"])
