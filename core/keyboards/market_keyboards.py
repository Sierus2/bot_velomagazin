from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.others.db_request import Request


async def kb_get_categories(request: Request):
    buttons = []

    categories = await request.db_get_categories()

    for category in categories:
        button = InlineKeyboardButton(
            text=category,
            callback_data=category

        )
        buttons.append(button)
    keyboards = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return keyboards


async def kb_get_subcategories(category, request: Request):
    buttons = []

    get_buttons = await request.db_get_subcategories(category)

    for get_button in get_buttons:
        button = InlineKeyboardButton(
            text=get_button,
            callback_data=get_button

        )
        buttons.append(button)
    back_button = InlineKeyboardButton(
        text='Назад',
        callback_data=f"back={category}"
    )

    new_button = [buttons]
    new_button.append([back_button])
    keyboards = InlineKeyboardMarkup(inline_keyboard=new_button)
    # print(19, keyboards)
    return keyboards


async def kb_get_items(request: Request, category, subcategory):
    buttons = []
    col_buttons = await request.db_get_items(category, subcategory)
    for col_button in col_buttons:
        model = col_button[0]
        price = col_button[1]
        button = InlineKeyboardButton(
            text=f"{model} ({price})",
            callback_data=f"description={model}|{price}"
        )
        buttons.append(button)
    back_button = InlineKeyboardButton(
        text='Орқага',
        callback_data=f"back={category}|{subcategory}"
    )
    new_list= [buttons]
    new_list.append([back_button])
    return InlineKeyboardMarkup(inline_keyboard=new_list)


async def kb_get_description(request: Request, product, category, subcategory):
    buttons = []
    col_button = await request.db_get_description(product[0], category, subcategory)

    model = col_button[0]
    price = col_button[1]

    button_cart = InlineKeyboardButton(
        text="Саватча",
        callback_data=f"cart={model}|{price}"
    )

    buttons.append(button_cart)
    button_back = InlineKeyboardButton(
        text="Orqaga",
        callback_data=f"back={category}|{subcategory}|{model}"
    )
    buttons.append(button_back)
    keyboards = InlineKeyboardMarkup(inline_keyboard=[buttons])
    text = f"Siz {product[0]} tovarini {product[1]} narxiga sotib olmoqchisiz. Sotuvni amalga oshiramizmi?"

    return text, keyboards


