from lib import dp, aiogtts, BytesIO, vk, aiohttp
from execute import VkFunction
from vk.keyboards import Keyboard
from vk import types
import json

send_25messages = VkFunction(args=("peer_id", "message"), clean_args=("peer_id",), code="""
var params = {"message": %(message)s, "peer_id": %(peer_id)s, "random_id": 0};
var i = 0;
while (i < 25) {
    API.messages.send(params);
    i = i + 1;
};
return true;
""")

keyboard = Keyboard(True)


@dp.message_handler(commands=["say"])
async def say_hello(message: types.Message, data: dict):
    io = BytesIO()
    args = message.get_args()
    await aiogtts.write_to_fp(" ".join(args[1:]), io, slow=True, lang=args[0])
    io.seek(0)
    result = await vk.api_request("docs.getMessagesUploadServer", dict(type="audio_message", peer_id=message.peer_id))
    url_data = aiohttp.FormData()
    url_data.add_field('file', io)
    async with vk.client.post(result["upload_url"], data=url_data) as response:
        result = await response.json()
    result = (await vk.api_request("docs.save", dict(file=result["file"])))["audio_message"]
    await message.answer("Hello!", attachment=f"doc{result['owner_id']}_{result['id']}")


@dp.message_handler(commands=["gen"])
async def spam_ls_key(message: types.Message, data: dict):
    keyboard = Keyboard(False)
    keyboard.add_text_button("/ " + message.text.split(" ", 1)[1], payload={"command": "spam"})
    keyboard.add_text_button("Убрать клавиатуру", payload={"command": "delete_keyboard"})
    await message.answer("Generated keyboard", keyboard=keyboard.get_keyboard())


@dp.message_handler(payload={"command": "delete_keyboard"})
async def delete_spam_ls(message: types.Message, data: dict):
    await message.answer("Deleted keyboard", keyboard=keyboard.get_empty_keyboard())


@dp.message_handler(payload={"command": "spam"})
async def spam_ls(message: types.Message, data: dict):
    await vk.api_request("execute", dict(**send_25messages(message.peer_id, message.text.split(" ", 1)[1])))
