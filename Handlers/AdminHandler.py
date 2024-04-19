import os

from dotenv import load_dotenv

from loader import bot

load_dotenv()


async def admin_message():
    await bot.send_message(os.environ.get("ADMIN_CHAT_ID"), "Бот запущен")
