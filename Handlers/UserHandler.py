from aiogram import types, F
from aiogram.filters import CommandStart
import requests
from Core.VoiceAssistant import voice_processing
from Keyboards.Reply.MainKeyboard import main_keyboard
from loader import dp, bot


@dp.message(CommandStart())
async def process_start_command(message: types.Message):
    await message.answer("Привет!", parse_mode='HTML', reply_markup=main_keyboard())


def generate_url(zapros):
    url = "https://www.google.com/search"

    params = {
        "q": zapros,
    }
    response = requests.get(url, params=params)
    return response.url


# @dp.message(F.content_type == 'voice')
# async def process_start_command(message: types.Message):
#     file_info = await bot.get_file(message.voice.file_id)
#     downloaded_file = await bot.download_file(file_info.file_path)
#
#     voice_text = voice_processing(downloaded_file)
#     command = voice_text.split()[0]
#     if command in ['Найди', 'найди', 'Поищи', 'поищи']:
#         link = generate_url(voice_text)
#         await message.answer(f"<a href='{link}'>Результат поиска</a>", parse_mode='HTML')
#     await message.answer(f"{voice_text}", parse_mode='HTML')


