from typing import Any, Optional

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.base import BaseSession

from bot.VPNBot import VPNBot


class AdminBot(Bot):
    def __init__(
        self,
        token: str,
        vpnBot: VPNBot,
        session: Optional[BaseSession] = None,
        default: Optional[DefaultBotProperties] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(token=token, session=session, default=default, **kwargs, )
        self.vpnBot = vpnBot
