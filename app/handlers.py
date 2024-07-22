import os

from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from dotenv import load_dotenv

from app.keyboards import generate_inline_keyboard, to_list_keyboard
from app.middlewares import TokensMiddleware

from aiogram import types, Router

from bot import bot

router = Router()

token_middleware = TokensMiddleware()
router.message.outer_middleware(token_middleware)

load_dotenv()
PARAM = os.getenv('START_PARAM')

NOT_ALLOWED = 'It seems that you are not allowed to use this bot :)'


@router.message(CommandStart(deep_link=True))
async def cmd_start(message: Message, command: CommandObject):
    args = command.args
    if args == PARAM:
        await message.answer(f'Hey!\nSelect a token:')
    else:
        await message.answer(NOT_ALLOWED)


@router.message(CommandStart())
async def cmd_start(message: Message):
    token_names = list(map(lambda x: x['name'], token_middleware.tokens))
    keyboard = generate_inline_keyboard(token_names)
    await message.answer(f'Hey!\nSelect a token:', reply_markup=keyboard)


@router.callback_query(lambda c: c.data == 'tokens_list')
async def process_tokens_list_callback(callback_query: types.CallbackQuery):
    token_names = list(map(lambda x: x['name'], token_middleware.tokens))
    keyboard = generate_inline_keyboard(token_names)
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Select a token:',
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data and c.data.startswith('page:'))
async def process_page_callback(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split(':')[1])
    token_names = list(map(lambda x: x['name'], token_middleware.tokens))
    keyboard = generate_inline_keyboard(token_names, page=page)
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data and c.data.startswith('item:'))
async def process_item_callback(callback_query: types.CallbackQuery):
    item = callback_query.data.split(':')[1]
    token = token_middleware.tokens_data.get_token(item)
    token_metrics = token_middleware.tokens_data.calc_token_metrics(item)
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=f"Token: {token['name']}\n\n"
             f"New holders: {token['new_users_min_amount']}\n\n"

             f"TVL category: {token['token_tvl_category']}\n"
             f"Start TVL: {token['token_start_tvl']} TON\n"
             f"Current TVL: {token['token_last_tvl']} TON\n"
             f"TVL Change: {token['token_tvl_change']} TON\n\n"

             f"Start price: {token['token_price_before']} TON\n"
             f"Current price: {token['token_price_after']} TON\n"
             f"Price change real: {token['price_change_simple']} %\n"
             f"Price change normed: {token['price_change_normed']} %\n\n"

             f"TVL category coefficient: {token_metrics['tvl_category_coefficient'] * 100} %\n\n"
             
             f"New holders weight: {token_metrics['new_holders_weight']} %\n"
             f"TVL change weight: {token_metrics['tvl_change_weight']} %\n"
             f"Price change weight: {token_metrics['price_change_weight']} %\n\n"
             
             f"New holders relative: {token_metrics['new_holders_relative']}\n"
             f"TVL change relative: {token_metrics['tvl_change_relative']}\n"
             f"Price change relative: {token_metrics['price_change_relative']}\n\n"

             f"Score from request: {token['score']}\n"
             f"Score calculated: {token_metrics['score']}\n"
    )
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=to_list_keyboard
    )
