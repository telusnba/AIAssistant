import asyncio
import os


from Handlers import dp
from Handlers.AdminHandler import admin_message
from loader import bot


async def main() -> None:
    await admin_message()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # loop = asyncio.get_event_loop()
    asyncio.run(main())
