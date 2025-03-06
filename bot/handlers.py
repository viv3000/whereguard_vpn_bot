from .keyboards import start_keyboard


async def start(answer):
    await answer("Привет! Этот бот предназначен для покупки VPN", reply_markup=start_keyboard)
