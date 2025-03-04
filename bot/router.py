from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters.command import Command

from bot.helpers import send_message_to_support

from bot.routers.FSMSupport import support_router
from bot.keyboards import start_keyboard
from bot.handlers import start


router = Router()
router.include_router(support_router)



@router.message(Command("start"))
async def cmd_start(message: Message):
    await start(message.answer)


@router.callback_query(F.data == "start")
async def call_start(call: CallbackQuery, bot: Bot):
    await start(call.message.answer)

