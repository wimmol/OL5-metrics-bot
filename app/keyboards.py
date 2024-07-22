from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ITEMS_PER_PAGE = 5


def generate_inline_keyboard(items, page=0):
    keyboard = []
    start = page * ITEMS_PER_PAGE * 2
    end = start + ITEMS_PER_PAGE * 2

    line = []
    for item in items[start:end]:
        if (items.index(item) + 1) % 2 == 0:
            line.append(InlineKeyboardButton(text=item, callback_data=f"item:{item}"))
            keyboard.append(line)
            line = []
        else:
            line.append(InlineKeyboardButton(text=item, callback_data=f"item:{item}"))

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="Previous", callback_data=f"page:{page - 1}"))
    if end < len(items):
        navigation_buttons.append(InlineKeyboardButton(text="Next", callback_data=f"page:{page + 1}"))

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


to_list_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text='To tokens list', callback_data='tokens_list')]])
