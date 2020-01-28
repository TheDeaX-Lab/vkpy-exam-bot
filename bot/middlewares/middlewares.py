from vk.bot_framework import BaseMiddleware, SkipHandler
from lib import dp


class MyMiddleware(BaseMiddleware):
    async def pre_process_event(self, event, data: dict):
        if event["type"] != "message_new":
            raise SkipHandler
        data["my_message"] = "Executed before handler"
        return data

    async def post_process_event(self):
        ...
