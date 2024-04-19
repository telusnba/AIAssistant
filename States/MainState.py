from aiogram.fsm.state import StatesGroup, State


class MyState(StatesGroup):
    state = State()


class ChatState(StatesGroup):
    ask = State()


class ImgState(StatesGroup):
    ask = State()
