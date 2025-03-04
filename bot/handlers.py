from .keyboards import start_keyboard


async def start(answer):
    await answer("Это текстовое сообщение!", reply_markup=start_keyboard)
