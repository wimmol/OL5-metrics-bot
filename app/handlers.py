import os

from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dotenv import load_dotenv

from app.classes.Simulation import Simulation
from app.keyboards import generate_inline_keyboard, choose_edit_keyboard, generate_token_keyboard
from app.middlewares import TokensMiddleware

from aiogram import types, Router

from app.utils.display_token_info import display_token_info
from bot import bot

router = Router()

token_middleware = TokensMiddleware()
router.message.outer_middleware(token_middleware)

load_dotenv()
PARAM = os.getenv('START_PARAM')

SELECT_TOKEN = '==== Hey! Select a token ====\n'


@router.message(CommandStart(deep_link=True))
async def cmd_start(message: Message, command: CommandObject):
    args = command.args
    if args == PARAM:
        token_names = list(map(lambda x: x['name'], token_middleware.tokens))
        keyboard = generate_inline_keyboard(token_names)
        await message.answer(SELECT_TOKEN, reply_markup=keyboard)
    else:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@router.callback_query(lambda c: c.data == 'tokens_list')
async def process_tokens_list_callback(callback_query: types.CallbackQuery):
    token_middleware.setTokens()
    token_names = list(map(lambda x: x['name'], token_middleware.tokens))
    keyboard = generate_inline_keyboard(token_names)
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=SELECT_TOKEN,
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data and c.data.startswith('simulate:'))
async def process_simulate_callback(callback_query: types.CallbackQuery, state: FSMContext):
    token_name = callback_query.data.split(':')[1]
    await state.update_data(token_name=token_name)
    await state.update_data(metrics={})
    await state.update_data(current_metric=None)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=f'Token: {token_name}\nChoose metric to edit:',
        reply_markup=choose_edit_keyboard
    )


@router.callback_query(lambda c: c.data and c.data.startswith('edit:'))
async def process_edit_callback(callback_query: types.CallbackQuery, state: FSMContext):
    metric = callback_query.data.split(':')[1]
    await state.set_state(Simulation.metrics)
    await state.update_data(current_metric=metric)
    message = await bot.send_message(
        text=f'Enter new value for {metric}:',
        chat_id=callback_query.message.chat.id
    )
    await state.update_data(message_to_delete_id=message.message_id)


@router.message(Simulation.metrics)
async def process_edit_message(message: Message, state: FSMContext):
    current_state = await state.get_data()
    metric = current_state['current_metric']
    new_metrics = current_state['metrics']
    new_metrics[metric] = message.text
    await state.update_data(metrics=new_metrics)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if current_state['message_to_delete_id'] is not None:
        await bot.delete_message(chat_id=message.chat.id, message_id=current_state['message_to_delete_id'])
        await state.update_data(message_to_delete_id=None)


@router.callback_query(lambda c: c.data == 'calculate')
async def process_calculate_callback(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_data()
    simulated_tokens = token_middleware.tokens_data
    for metric in current_state['metrics']:
        if metric == 'new_current_price':
            simulated_tokens.input_new_current_price(current_state['token_name'], float(current_state['metrics'][metric]))
        elif metric == 'new_current_tvl':
            simulated_tokens.input_new_current_tvl(current_state['token_name'], float(current_state['metrics'][metric]))
        elif metric == 'new_current_new_holders':
            simulated_tokens.input_new_current_holders(
                current_state['token_name'], float(current_state['metrics'][metric]))
        elif metric == 'max_new_holders':
            simulated_tokens.max_new_holders = float(current_state['metrics'][metric])
        elif metric == 'max_tvl_change':
            simulated_tokens.max_tvl_change = float(current_state['metrics'][metric])
        elif metric == 'max_price_change':
            simulated_tokens.max_price_change = float(current_state['metrics'][metric])
        elif metric == 'min_tvl_change':
            simulated_tokens.min_tvl_change = float(current_state['metrics'][metric])
        elif metric == 'min_price_change':
            simulated_tokens.min_price_change = float(current_state['metrics'][metric])
    simulated_tokens.calc_token_metrics(current_state['token_name'], force=True)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=display_token_info(simulated_tokens.get_token(current_state['token_name']))
    )
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=generate_token_keyboard(current_state['token_name'])
    )
    await state.clear()


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
    token = token_middleware.tokens_data.calc_token_metrics(item)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=display_token_info(token)
    )
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=generate_token_keyboard(item)
    )


@router.message()
async def cmd_start(message: Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

# await message.answer('The Open League 5\nTokens metrics bot',
# reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
# text='Get access', url='https://t.me/gpirj32xk253hjk3_bot?start=dont-share-this-link')]]))
