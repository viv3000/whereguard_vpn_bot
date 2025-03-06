from aiogram import Bot
from aiogram.types import User

from services.entities import UserBuilder, VPNUser


def test_create_user():
    test_user = User(id=12345, is_bot=False, first_name="test")
    builder = UserBuilder(test_user)
    user = builder.build()
    assert user.user_data.__dict__ == VPNUser(test_user).user_data.__dict__
    assert user.__dict__ == VPNUser(test_user).__dict__
