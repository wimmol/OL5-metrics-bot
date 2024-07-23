from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ITEMS_PER_PAGE = 5


def generate_inline_keyboard(items, page=0):
    keyboard = []
    start = page * ITEMS_PER_PAGE * 2
    end = start + ITEMS_PER_PAGE

    for i in range(start, end, 1):
        keyboard.append([InlineKeyboardButton(text=f'{i + 1}. {items[i]}', callback_data=f"item:{items[i]}"),
                         InlineKeyboardButton(text=f'{i + 1 + ITEMS_PER_PAGE}. {items[i + ITEMS_PER_PAGE]}',
                                              callback_data=f"item:{items[i + ITEMS_PER_PAGE]}")])

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="Previous", callback_data=f"page:{page - 1}"))
    if end < len(items):
        navigation_buttons.append(InlineKeyboardButton(text="Next", callback_data=f"page:{page + 1}"))

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def generate_token_keyboard(token_name):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text='To tokens list', callback_data='tokens_list')], [InlineKeyboardButton(
            text='Simulate', callback_data=f'simulate:{token_name}')]])


choose_edit_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='new holders', callback_data='edit:new_current_new_holders'),
    ],
    [
        InlineKeyboardButton(text='current tvl', callback_data='edit:new_current_tvl'),
        InlineKeyboardButton(text='current price', callback_data='edit:new_current_price')
    ],
    [
        InlineKeyboardButton(text='max new holders', callback_data='edit:max_new_holders'),
    ],
    [
        InlineKeyboardButton(text='max tvl change', callback_data='edit:max_tvl_change'),
        InlineKeyboardButton(text='max price change', callback_data='edit:max_price_change'),
    ],
    [
        InlineKeyboardButton(text='min tvl change', callback_data='edit:min_tvl_change'),
        InlineKeyboardButton(text='min price change', callback_data='edit:min_price_change'),
    ],
    [
        InlineKeyboardButton(text='Calculate', callback_data='calculate'),
    ]
])
