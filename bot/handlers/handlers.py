from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardRemove

from bot.core.crud import get_addres_by_id, get_six_code_by_id, get_private_key
from bot.handlers.validator import check_id_duplicate, check_code_duplicate
from bot.handlers.keyboard_button import (
    WALLET,
    DEPOSIT,
    RATING,
    REFERRAL_PROGRAM,
    CREATE, GET, SEND, EXCHANGE, STARTMENU,
    KWEI, MWEI, GWEI, MICROETHER, ETHER,
    DAO_IN_USDC, REQUEST_USDC,
    DAO_IN_W3, REQUEST_W3,
    DAO_FROM_W3_TO_USDT, REQUEST_W3_USDT
)
from bot.handlers.states import SixCode, Transaction, DAOTRANSITION
from bot.arbitrum.arbitrum import create_wallet, arb_get_balanse, send_currency
from bot.nowpayments.api import create_pay

router = Router()


@router.message(F.text == STARTMENU)
@router.message(CommandStart())
async def command_start(
    message: types.Message,
) -> None:
    await message.answer(
        'Hi! what do you want?',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=WALLET),
                    KeyboardButton(text=DEPOSIT),
                    KeyboardButton(text=RATING),
                    KeyboardButton(text=REFERRAL_PROGRAM),
                ]
            ],
        ),
    )


@router.message(F.text == WALLET)
async def command_start(
    message: types.Message,
) -> None:
    if (
        await check_id_duplicate(message.from_user.id) == False
    ):
        await message.answer(
            f'You have a wallet, choise optoin',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=STARTMENU),
                        KeyboardButton(text=GET),
                        KeyboardButton(text=SEND),
                        KeyboardButton(text=EXCHANGE),
                    ]
                ],
            ),
        )
    else:
        await message.answer(
            'Hi! what do you want?',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=CREATE),
                        KeyboardButton(text=GET),
                        KeyboardButton(text=SEND),
                        KeyboardButton(text=EXCHANGE),
                    ]
                ],
            ),
        )


@router.message(F.text == CREATE)
async def wallet_start_window(message: Message, state: FSMContext) -> None:
    await state.set_state(SixCode.six_code)
    await message.answer(
        "Enter six digit code",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(SixCode.six_code)
async def state_wallet(message: Message, state: FSMContext) -> None:
    if (
        (
            await check_code_duplicate(message.text) == True
        ) or (
            message.text.isdigit() == False
        )
        or (len(message.text) > 6)
    ):
        await message.answer(
            f"U send not valid code or code is use",
            reply_markup=ReplyKeyboardRemove(),
        )
        await wallet_start_window(message)
    address, seed_phrase = await create_wallet(
        user_id=message.from_user.id,
        six_code=message.text
    )
    await message.answer(
        f"Wallet created!Address: \n{address} \nSeed Phrase: {seed_phrase}",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=STARTMENU),
                ]
            ],
        ),
    )
    await state.clear()


@router.message(F.text == GET)
async def wallet_get(message: Message) -> None:
    result = await get_addres_by_id(message.from_user.id)
    if result is not None:
        await message.answer(
            f'Your crypto wallet address `{result}`',
            parse_mode='MarkdownV2'
        )
    else:
        await message.answer(
            "You don't have a wallet, let's create one?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=CREATE),
                    ]
                ],
            ),
        )


@router.message(F.text == SEND)
async def wallet_send(message: Message, state: FSMContext) -> None:
    await state.set_state(Transaction.address)
    await message.answer(
        "Enter address",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Transaction.address)
async def wallet_get_currency(message: Message, state: FSMContext) -> None:
    address = message.text
    if await arb_get_balanse(address, ETHER) is None:
        await message.answer(
            "The wallet address was entered incorrectly",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=STARTMENU),
                    ]
                ],
                resize_keyboard=True
            ),
        )
    else:
        await state.set_state(Transaction.currency)
        await message.answer(
            "Choose currency",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=ETHER),
                        KeyboardButton(text=MICROETHER),
                        KeyboardButton(text=GWEI),
                        KeyboardButton(text=MWEI),
                        KeyboardButton(text=KWEI),
                    ]
                ],
                resize_keyboard=True
            ),
        )


@router.message(Transaction.currency)
async def wallet_get_amount(message: Message, state: FSMContext) -> None:
    await state.set_state(Transaction.amount)
    await message.answer(
        "Enter the number of coins to send",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Transaction.amount)
async def wallet_get_six_code(message: Message, state: FSMContext) -> None:
    if (message.text).isdigit() == False:
        await message.answer(
            "You entered the number incorrectly (you only need to send numbers)",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=STARTMENU),
                    ]
                ],
            ),
        )
    elif await arb_get_balanse(
        address=await get_addres_by_id(
            message.from_user.id
        ),
        currency=message.text
    ) < int(message.text):
        await message.answer(
            "You do not have sufficient funds to complete the transaction. Check your balance",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=STARTMENU),
                    ]
                ],
            ),
        )
    else:
        await state.set_state(Transaction.six_code)
        await message.answer(
            "Enter six-code",
            reply_markup=ReplyKeyboardRemove(),
        )


@router.message(Transaction.six_code)
async def wallet_check_six_code(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if await get_six_code_by_id(message.from_user.id) == int(message.text):
        tx_hex = await send_currency(
            sender_address=get_addres_by_id(message.from_user.id),
            recipient_address=data.get('address'),
            private_key=await get_private_key(message.from_user.id),
            amount=data.get('amount')
        ),
        await message.answer(
            f'Trans {tx_hex}',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=STARTMENU),
                    ]
                ],
            ),
        )
    else:
        await message.answer(
            "Invalid 6-digit code",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=STARTMENU),
                    ]
                ],
            ),
        )


@router.message(F.text == DEPOSIT)
async def depozit(message: Message):
    await message.answer(
        f'Choise optoin',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=DAO_IN_USDC),
                    KeyboardButton(text=REQUEST_USDC),
                    KeyboardButton(text=REQUEST_W3),
                    KeyboardButton(text=DAO_IN_W3),
                    KeyboardButton(text=DAO_FROM_W3_TO_USDT),
                    KeyboardButton(text=REQUEST_W3_USDT),
                    KeyboardButton(text=STARTMENU),
                ]
            ],
        ),
    )


@router.message(F.text == DAO_IN_USDC)
async def dao_in_usdc(message: Message, state: FSMContext):
    await message.answer(
        f'In the form of the $USDC amount you want to make a deposit?',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=STARTMENU),
                ]
            ],
        ),
    )
    await state.set_state(DAOTRANSITION.amount)


@router.message(DAOTRANSITION.amount)
async def dao_in_usdcf(message: Message, state: FSMContext):
    if int(message.text) <= 0:
        await message.answer(
            f'Number less than zero {message.text}',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=STARTMENU),
                    ]
                ],
            ),
        )

    elif (message.text).isdigit() == False:
        await message.answer(
            "Number cannot contain letters",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=STARTMENU),
                    ]
                ],
            ),
        )
    else:
        amount = int(message.text)
        await state.update_data(amount=amount)
        nigga = create_pay(int(message.text))
        url_for_pay = nigga.get('invoice_url')
        await message.answer(
            f'{url_for_pay} - copy ETH adress and send me {message.text}',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=STARTMENU),
                    ]
                ],
            ),
        )
        await state.set_state(DAOTRANSITION.wallet_adress)


@router.message(DAOTRANSITION.wallet_adress)
async def put_adress(message: Message, state: FSMContext):
    data = await state.get_data()
    m = data.get('amount')
    if await arb_get_balanse(message.text, 'gwei') is None:
        await message.answer(
            f'Copy ETH address and send again ',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=STARTMENU),
                    ]
                ],
            ),
        )
    await state.update_data(wallet_adress=message.text)
    await message.answer(
        f'Six code {m}',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=STARTMENU),
                ]
            ],
        ),
    )
    await state.set_state(DAOTRANSITION.six_code)


@router.message(DAOTRANSITION.six_code)
async def dao_six_code(message: Message, state: FSMContext):
    data = await state.get_data()
    if await get_six_code_by_id(message.from_user.id) == int(message.text):
        tx_hex = await send_currency(
            sender_address=await get_addres_by_id(message.from_user.id),
            recipient_address=str(data.get('wallet_adress')),
            private_key=await get_private_key(message.from_user.id),
            amount=data.get('amount'),
        )
        await message.answer(
            f'Trans {tx_hex}. Wait 20min for confirm transaction',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=STARTMENU),
                    ]
                ],
            ),
        )
    else:
        await message.answer(
            "Invalid 6-digit code, try again",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=STARTMENU),
                    ]
                ],
            ),
        )
        await dao_six_code()
