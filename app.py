from lib import task_manager, dp, vk, asyncio
import bot.handlers
from bot.middlewares import MyMiddleware


async def run():
    dp.setup_middleware(MyMiddleware())
    await dp.run_polling()


async def on_startup():
    print("Started!")


async def on_shutdown():
    await vk.close()
    await asyncio.sleep(0.250)
    print("Closed!")

if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(on_startup=on_startup, on_shutdown=on_shutdown)
    task_manager.close()
