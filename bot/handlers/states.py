from aiogram.fsm.state import StatesGroup, State


class SixCode(StatesGroup):
    six_code = State()


class Transaction(StatesGroup):
    address = State()
    currency = State()
    amount = State()
    six_code = State()


class DAOTRANSITION(StatesGroup):
    amount = State()
    wallet_adress = State()
    six_code = State()
