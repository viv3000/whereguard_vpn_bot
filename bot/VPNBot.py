import json

from typing import Any, Optional

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.base import BaseSession


def get_messages():
    messages = None

    with open('messages.json', 'r') as file:
        messages = json.load(file)

    return messages

class VPNBot(Bot):
    messages = get_messages()

    def __init__(
        self,
        token: str,
        pay_token: str,
        support_chat_id: int,
        messages,
        session: Optional[BaseSession] = None,
        default: Optional[DefaultBotProperties] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(token=token, session=session, default=default, **kwargs, )
        self.pay_token = pay_token
        self.support_chat_id = support_chat_id
        self.messages = VPNBot.messages
