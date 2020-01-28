from lib import dp
from vk import types


@dp.message_handler(chat_action=types.message.Action.chat_invite_user)
async def on_invite_member_handler(message: types.Message, data: dict):
    await message.answer("Hello, you invited!")


@dp.message_handler(chat_action=types.message.Action.chat_kick_user)
async def on_kick_member_handler(message: types.Message, data: dict):
    await message.answer("Goodbye!")


@dp.message_handler()
async def on_message_handler(message: types.Message, data: dict):
    await message.answer(str(message.get_args()))
