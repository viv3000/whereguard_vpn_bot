from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters.command import Command

from bot.VPNBot import VPNBot
from bot.routers.FSMSupport import support_router
from bot.routers.pay import pay_router
from bot.routers.menu import menu_router
from bot.handlers import start


router = Router()
router.include_router(support_router)
router.include_router(pay_router)
router.include_router(menu_router)


@router.message(Command("start"))
async def cmd_start(message: Message, bot: VPNBot):
    await start(message, message.from_user, bot.messages)


@router.callback_query(F.data == "start")
async def call_start(call: CallbackQuery, bot: VPNBot):
    await start(call.message, call.from_user, bot.messages)


@router.message(F.text == VPNBot.messages["buttons"]["start"])
async def message_start(message: Message, bot: VPNBot):
    await message.answer(bot.messages["greetings_first"])
