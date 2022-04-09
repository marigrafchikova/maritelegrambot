
from email.message import Message
import os
import handlers
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from data.config import ADMINS, WEBHOOK_PATH, WEBHOOK_URL

from loader import dp, db, bot
import filters
import logging

filters.setup(dp)

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 5000))
user_message = 'Пользователь'
admin_message = 'Админ'
menu_message = '/menu'

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    

    markup.row(user_message, admin_message)
    
    await message.answer('''Привет! 👋

🤖 Я бот-магазин по подаже товаров любой категории.
    
🛍️ Чтобы перейти в каталог и выбрать приглянувшиеся товары возпользуйтесь командой /menu.

💰 Пополнить счет можно через Яндекс.кассу, Сбербанк или Qiwi.

❓ Возникли вопросы? Не проблема! Команда /sos поможет связаться с админами, которые постараются как можно быстрее откликнуться.

🤝 Заказать похожего бота? <a href="https://t.me/svnstm">Свяжитесь</a> с разработчиком.
    ''', reply_markup=markup)


@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
    markup_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    markup_menu.insert(menu_message)
    cid = message.chat.id
    if cid in ADMINS:
        ADMINS.remove(cid)


    # await message.answer('', reply_markup=ReplyKeyboardRemove())
    await message.answer('Включен пользовательский режим.', reply_markup=markup_menu)


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):
    markup_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    markup_menu.insert(menu_message)
    cid = message.chat.id
    if cid not in ADMINS:
        ADMINS.append(cid)


    # await message.answer('', reply_markup=ReplyKeyboardRemove())
    await message.answer('Включен админский режим.', reply_markup=markup_menu)
    

async def on_startup(dp):
    logging.basicConfig(level=logging.INFO)
    db.create_tables()

    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown():
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == '__main__':

    if "HEROKU" in list(os.environ.keys()):

        executor.start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )

    else:

        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
