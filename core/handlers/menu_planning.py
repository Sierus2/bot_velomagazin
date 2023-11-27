from typing import List

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.keyboards.market_keyboards import kb_get_categories, kb_get_subcategories, kb_get_items, kb_get_description
from core.others.db_request import Request


async def get_categories(message: Message, bot: Bot, request: Request):
    await message.answer(
        "<b>Salom! Men 'ABS' internet do'koni yordamchisiman.</b> \r\n\r\n Keling sizga menyuni ko'rsataman!",
        reply_markup=await kb_get_categories(request))


async def management(call: CallbackQuery, bot: Bot, state: FSMContext, request: Request):
    if 'description' in call.data:
        product = call.data.split('=')[1].split('|')
        category = call.message.reply_markup.inline_keyboard[-1][-1].callback_data.split('=')[1].split('|')[0]
        subcategory = call.message.reply_markup.inline_keyboard[-1][-1].callback_data.split('=')[1].split('|')[1]
        text, keyboards = await kb_get_description(request, product, category, subcategory)
        return await call.message.edit_text(text, reply_markup=keyboards)

    elif 'back' in call.data:
        data_back = call.data.split('=')[1]
        path = data_back.split('|')

        if len(path) == 3:
            category = path[0]
            subcategory = path[1]
            await call.message.edit_text('Men sizga yana bularni ham tavsiya eta olaman',
                                         reply_markup=await kb_get_items(request, category, subcategory))
        elif len(path) == 2:
            category = path[0]
            await call.message.edit_reply_markup(reply_markup=await kb_get_subcategories(category, request))
        else:
            await call.message.edit_reply_markup(reply_markup=await kb_get_categories(request))
    else:
        if await is_back(call.message.reply_markup.inline_keyboard):
            category = call.message.reply_markup.inline_keyboard[-1][-1].callback_data.split('=')[1].split('|')[0]
            subcategory = call.data
            keyboards = await kb_get_items(request, category, subcategory)
        else:
            keyboards = await kb_get_subcategories(str(call.data), request)
        await call.message.edit_reply_markup(reply_markup=keyboards)


async def is_back(keyboards: List[List]):
    for keyboard in keyboards:
        for element in keyboard:
            if 'back' in element.callback_data:
                return True
    return False
