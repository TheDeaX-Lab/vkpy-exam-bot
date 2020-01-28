from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher
from vk.constants import JSON_LIBRARY
import asyncio
import logging
from io import BytesIO
from aiogtts import aiogTTS
import aiohttp


with open("config.json", "r") as config:
    config = JSON_LIBRARY.load(config)

logging.basicConfig(
    level=config["logging_level"],
    format="%(asctime)s - %(levelname)s:: %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}".format(config["logging_path"],
                                             config["logging_file"])),
        logging.StreamHandler()
    ]
)

vk = VK(config["token"])
task_manager = TaskManager(vk.loop)
dp = Dispatcher(vk, config["group_id"])
api = vk.get_api()
aiogtts = aiogTTS()
