from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_keyboard():
    main_kb = ReplyKeyboardBuilder()

    main_kb.button(text='/chat')
    main_kb.button(text='/img')
    main_kb.adjust(2)
    return main_kb.as_markup()


def clear_keyboard():
    clear_kb = ReplyKeyboardBuilder()

    clear_kb.button(text='/clear')
    clear_kb.adjust(2)
    return clear_kb.as_markup()
