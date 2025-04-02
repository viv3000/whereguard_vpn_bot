import logging

from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from bot.VPNBot import VPNBot
from bot.handlers import start
from bot.helpers import send_message_to_support
from bot.keyboards import cancel_keyboard

support_router = Router()
storage = MemoryStorage()

class FormSupport(StatesGroup):
    support_message = State()


@support_router.callback_query(F.data == "support", StateFilter(default_state))
async def call_support(call: CallbackQuery, state: FSMContext, bot: VPNBot):
    try:
        await call.message.answer(text=bot.messages["suport"], reply_markup=cancel_keyboard(bot.messages))
        await state.set_state(FormSupport.support_message)
        logging.info(f"start support: {call.from_user.username}")
    except Exception as exception:
        logging.error(f"error in start support: {call.from_user.username}", exc_info=True)


@support_router.message(F.text == VPNBot.messages["buttons"]["support"], StateFilter(default_state))
async def message_support(message: Message, state: FSMContext, bot: VPNBot):
    try:
        await message.answer(text=bot.messages["suport"], reply_markup=cancel_keyboard(bot.messages))
        await state.set_state(FormSupport.support_message)
        logging.info(f"start support: {message.from_user.username}")
    except Exception as exception:
        logging.error(f"error in start support: {message.from_user.username}", exc_info=True)



@support_router.message(F.text, FormSupport.support_message)
async def capture_support(message: Message, state: FSMContext, bot: VPNBot):
    try:
        if message.text == bot.messages["buttons"]["cancel"]: 
            await start(message, message.from_user, bot.messages)
            await state.clear()
        else:
            await state.update_data(support_message=FormSupport.support_message)
            await message.answer(text=bot.messages["after_support"])
            await send_message_to_support(message.text, message.from_user, bot)
            await start(message, message.from_user, bot.messages)
            logging.info(f"send message: {message.text.encode()} to suport support: {message.from_user.username}")
            await state.clear()
    except Exception as exception:
        await state.clear()
        logging.error(f"error in start support: {message.from_user.username}", exc_info=True)
