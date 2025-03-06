from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters.command import Command

from bot.routers.FSMSupport import support_router
from bot.routers.pay import pay_router
from bot.handlers import start


router = Router()
router.include_router(support_router)
router.include_router(pay_router)


@router.message(Command("start"))
async def cmd_start(message: Message):
    await start(message.answer)


@router.callback_query(F.data == "start")
async def call_start(call: CallbackQuery):
    await start(call.message.answer)

