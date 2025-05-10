from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.filters.command import Command

from admin_bot.AdminBot import AdminBot
from log import logError, logInfo
from services.data import Data


admin_router = Router()

admin_text = {
        'start': "Это всего лишь админка, сосунок, не зазнавайся!",
        'commands': '\n'.join([
            '/start', 
            '/get_all_users',
            '/newsletter_message',
            '/send_message'
        ]),

        'send_massage_start': 'для отмены /cancel\nСообщение:',
        'send_massage_get_user_id': 'для отмены /cancel\nid пользователя:',

        'send_newsletter_start': 'для отмены /cancel\nСообщение:',
}


@admin_router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(text=f"{admin_text['start']}\n{admin_text['commands']}")


@admin_router.message(Command("get_all_users"))
async def cmd_get_all_users(message: Message):
    users = Data.get_all_users()
    users_keys = []
    users_text = 'username: tg id, (peer, expiration date)\n'
    for user in users:
        users_text += f'@{user.tg_name}: {user.tg_id} ({user.peer_id} {user.expiration_date})\n'
        users_keys.append(KeyboardButton(text=f'{user.tg_id}'))

    await message.answer(text=users_text, reply_markup=None)
    await message.answer(text=admin_text['commands'])


storage = MemoryStorage()

class FormSendMessage(StatesGroup):
    message = State()
    tg_id = State()

@admin_router.message(Command("send_message"), StateFilter(default_state))
async def cmd_send_message_start(message: Message, state: FSMContext):
    if (message.text == "/cancel"): 
        await state.clear()
        await message.answer(text=admin_text['commands'])
        return
    try:
        users = Data.get_all_users()
        users_keys = []
        users_text = ''
        for user in users:
            users_text += f'{user.tg_name}: {user.tg_id}\n'
            users_keys.append(KeyboardButton(text=f'{user.tg_id}'))

        users_keyboard = ReplyKeyboardMarkup(keyboard=[
            users_keys,
        ])

        await message.answer(text=users_text, reply_markup=users_keyboard)
        await message.answer(text=admin_text["send_massage_get_user_id"], reply_markup=users_keyboard)

        await state.set_state(FormSendMessage.tg_id)
        logInfo(f"admin: start send message", message.from_user)
    except Exception as exception:
        logError(f"error in start support", message.from_user)


@admin_router.message(F.text, FormSendMessage.tg_id)
async def send_message_capture_message(message: Message, state: FSMContext):
    if (message.text == "/cancel"): 
        await state.clear()
        await message.answer(text=admin_text['commands'])
        return
    try:
        await state.update_data(tg_id=message.text)
        await message.answer(text=admin_text["send_massage_start"])
        await state.set_state(FormSendMessage.message)
        logInfo(f"admin: start send message", message.from_user)
    except Exception as exception:
        logError(f"error in start support", message.from_user)


@admin_router.message(F.text, FormSendMessage.message)
async def send_message_capture_tg_id(message: Message, state: FSMContext, bot: AdminBot):
    if (message.text == "/cancel"): 
        await state.clear()
        await message.answer(text=admin_text['commands'])
        return
    try:
        await state.update_data(message=message.text)
        send_message_data = await state.get_data()
        await bot.vpnBot.send_message(chat_id=send_message_data['tg_id'], text=send_message_data['message'])
        await message.answer(text="Готово")
        await state.clear()
        await message.answer(text=admin_text['commands'])
    except Exception as exception:
        await state.clear()
        await message.answer(text=admin_text['commands'])



class FormSendNewsletter(StatesGroup):
    message = State()

@admin_router.message(Command("newsletter_message"), StateFilter(default_state))
async def cmd_send_newsletter_start(message: Message, state: FSMContext):
    if (message.text == "/cancel"): 
        await state.clear()
        await message.answer(text=admin_text['commands'])
        return
    try:
        await message.answer(text=admin_text["send_massage_start"])

        await state.set_state(FormSendNewsletter.message)
        logInfo(f"admin: start send message to newsletter", message.from_user)
    except Exception as exception:
        logError(f"error in start support", message.from_user)


@admin_router.message(F.text, FormSendNewsletter.message)
async def cmd_send_newsletter_capture_message(message: Message, state: FSMContext, bot: AdminBot):
    if (message.text == "/cancel"): 
        await state.clear()
        await message.answer(text=admin_text['commands'])
        return
    try:
        await state.update_data(message=message.text)
        users = Data.get_all_users()
        for user in users:
            await bot.vpnBot.send_message(chat_id=user.tg_id, text=message.text)

        await state.clear()
        await message.answer(text="Готово")
        await message.answer(text=admin_text['commands'])
    except Exception as exception:
        await state.clear()
        await message.answer(text=admin_text['commands'])



