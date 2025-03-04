from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import start
from bot.helpers import send_message_to_support

support_router = Router()
storage = MemoryStorage()

class FormSupport(StatesGroup):
    support_message = State()


@support_router.callback_query(F.data == "support", StateFilter(default_state))
async def call_support(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text="Запрос в ТП:")


@support_router.message(F.text, StateFilter(default_state))
async def capture_support(message: Message, state: FSMContext, bot: Bot):
    await state.set_state(FormSupport.support_message)
    await send_message_to_support(message.text, message.from_user, bot)
    await start(message.answer)
