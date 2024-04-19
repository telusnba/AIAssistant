import os

from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from Core.ImgAssistant import get_dalle_response
from Core.VoiceAssistant import voice_processing
from Keyboards.Inline.CancelKeyboard import cancel_menu
from States.MainState import ImgState
from loader import dp, bot

load_dotenv()


@dp.message(Command('img'))
async def prompt_img(message: types.Message, state: FSMContext):
    if str(message.from_user.id) == os.environ.get("ADMIN_CHAT_ID"):
        await message.answer(f"Введи запрос", parse_mode='HTML', reply_markup=cancel_menu)
        await state.set_state(ImgState.ask)
    else:
        await message.answer(f"❗У вас нету прав❗️", parse_mode='HTML', reply_markup=cancel_menu)


@dp.message(ImgState.ask)
async def process_prompt_img(message: types.Message, state: FSMContext):
    try:
        user_input = message.text
        if message.content_type == types.ContentType.VOICE:
            file_info = await bot.get_file(message.voice.file_id)
            downloaded_file = await bot.download_file(file_info.file_path)
            user_input = voice_processing(downloaded_file)
        process_answer = await message.answer(f"♻️♻️♻️", parse_mode='HTML')
        dalle_response_url = await get_dalle_response(user_input)
        print(dalle_response_url)
        media = [types.InputMediaPhoto(media=url) for url in dalle_response_url]
        await bot.delete_message(chat_id=message.from_user.id, message_id=process_answer.message_id)
        await message.answer_media_group(media, parse_mode='HTML', reply_markup=cancel_menu)
    except Exception:
        await message.answer(f"❗️Ошибка❗️", parse_mode='HTML', reply_markup=cancel_menu)
        await state.set_state(ImgState.ask)
