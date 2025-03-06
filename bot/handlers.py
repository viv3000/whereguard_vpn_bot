from .keyboards import start_keyboard


async def start(answer):
    await answer("Привет! Этот бот предназначен для покупки VPN", reply_markup=start_keyboard)


async def get_config(answer):
    await answer("Установи приложение wireguard\n <a href='https://play.google.com/store/apps/details?id=com.wireguard.android&hl=ru'>windows</a>\n<a href='https://play.google.com/store/apps/details?id=com.wireguard.android'>android</a>\n<a href='https://apps.apple.com/ru/app/wireguard/id1441195209'>ios</a>\n<a href='https://www.wireguard.com/install/'>остальное</a>")
