from aiogram.fsm.state import StatesGroup, State


class SixCode(StatesGroup):
    six_code = State()


class Transaction(StatesGroup):
    address = State()
    amount = State()
    currency = State()
    six_code = State()
