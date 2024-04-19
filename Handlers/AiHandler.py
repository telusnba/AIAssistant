from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from Core.AiAssistant import trim_history, get_gpt_response
from Core.VoiceAssistant import voice_processing
from Keyboards.Inline.CancelKeyboard import cancel_menu
from Keyboards.Reply.MainKeyboard import clear_keyboard, main_keyboard
from States.MainState import ChatState
from loader import dp, bot

conversation_history = {}


@dp.message(Command('chat'))
async def prompt_chat(message: types.Message, state: FSMContext):
    await message.answer(f"Введи запрос", parse_mode='HTML', reply_markup=cancel_menu)
    await state.set_state(ChatState.ask)


@dp.message(ChatState.ask)
async def process_prompt_chat(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        user_input = message.text
        if message.content_type == types.ContentType.VOICE:
            file_info = await bot.get_file(message.voice.file_id)
            downloaded_file = await bot.download_file(file_info.file_path)
            user_input = voice_processing(downloaded_file)
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        process_answer = await message.answer(f"♻️♻️♻️", parse_mode='HTML')

        if isinstance(user_input, str):
            conversation_history[user_id].append({"role": "user", "content": user_input})
            conversation_history[user_id] = trim_history(conversation_history[user_id])
        else:
            await message.answer(f"❗️Ошибка❗️\n"
                                 f"Введи текст или голосове сообщение!", parse_mode='HTML', reply_markup=cancel_menu)
            await state.set_state(ChatState.ask)

        chat_history = conversation_history[user_id]
        chat_gpt_response = get_gpt_response(chat_history)

        conversation_history[user_id].append({"role": "assistant", "content": chat_gpt_response})
        print(conversation_history)
        length = sum(len(message["content"]) for message in conversation_history[user_id])
        print(length)
        await bot.delete_message(chat_id=message.from_user.id, message_id=process_answer.message_id)
        await message.answer(f"{chat_gpt_response}", parse_mode='HTML', reply_markup=cancel_menu)
    except Exception:
        await message.answer(f"❗️Ошибка❗️", parse_mode='HTML', reply_markup=cancel_menu)
        await state.set_state(ChatState.ask)


@dp.message(Command('clear'))
async def process_clear_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    conversation_history[user_id] = []
    await state.clear()
    await message.reply("История диалога очищена.", reply_markup=main_keyboard())
