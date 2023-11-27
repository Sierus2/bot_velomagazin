from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message

from core.others.db_request import Request
from core.settings import settings


async def clear_cart(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await bot.answer_callback_query(call.id)
    await call.message.answer(f"{call.message.chat.first_name}, sizning savatchangiz tozalandi!")


async def send_invoice(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()

    price = []

    for k, v in data.items():
        price.append(
            LabeledPrice(
                label=k,
                amount=int(v) * 100 * 12298
            )
        )

    title = "Велосипед магазинидан онлайн харид"
    description = f"Тўлов амалга оширилиши билан менежерлар сизга қўнғироқ қилади.\r\n"

    await bot.send_invoice(
        chat_id=call.message.chat.id,
        title=title,
        description=description,
        payload='telegram_order',
        provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
        currency='uzs',
        prices=price,
        need_name=True,
        need_phone_number=True,
        is_flexible=False
    )


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot, message:Message):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    text = (f"👤 <b>To'lovchi:</b> {pre_checkout_query.from_user.first_name}\r\n"
            f"📞 <b>Telefon raqami:</b> {pre_checkout_query.order_info.phone_number}\r\n"
            f"💴 <b>Summa:</b> {pre_checkout_query.total_amount / 100}")
    # await bot.send_message(settings.bots.admin_id, text=dict_line(dict(pre_checkout_query)))
    await bot.send_message(chat_id=message.chat.id, text=text)


async def buy_complete(message: Message, state: FSMContext, bot: Bot, request: Request):
    msg = f"To'lovingiz uchun tashakkur!\r\n\r\nSumma: {message.successful_payment.total_amount // 100} {message.successful_payment.currency}"
    await bot.send_message(chat_id=message.chat.id, text=msg)


