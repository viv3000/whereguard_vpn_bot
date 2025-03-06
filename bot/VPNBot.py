from typing import Any, Optional

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.base import BaseSession


class VPNBot(Bot):
    def __init__(
        self,
        token: str,
        pay_token: str,
        session: Optional[BaseSession] = None,
        default: Optional[DefaultBotProperties] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(token=token, session=session, default=default, **kwargs, )
        self.pay_token = pay_token
