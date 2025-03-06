from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters.command import Command

from bot.routers.FSMSupport import support_router
from bot.routers.pay import pay_router
from bot.handlers import get_config, start


menu_router = Router()


@menu_router.callback_query(F.data == "get_config")
async def call_get_config(call: CallbackQuery):
    await get_config(call.message, call.from_user)
    await start(call.message, call.from_user)


@menu_router.callback_query(F.data == "get_date")
async def call_get_date(call: CallbackQuery):
    await start(call.message, call.from_user)


