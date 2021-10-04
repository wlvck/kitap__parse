import re

from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import urllib.request
import requests
from bs4 import BeautifulSoup as bs
from keyboards.default.category_menu import category_menu, read_file, category_returner
from loader import dp, bot
import os

API_TOKEN = '933uix5DGvQBs0V1'


@dp.message_handler(Command('kitap'))
async def bot_start(message: types.Message):
    await message.answer('Бөлімдердің бірін таңдаңыз', reply_markup=category_menu)


for main_category in read_file:
    @dp.message_handler(text=main_category)
    async def answer(message: types.Message):
        keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for category in read_file[message.text]:
            button = KeyboardButton(text=category['category_title'])
            keyboard.insert(button)

        bakc_to_main_categories = KeyboardButton('Негізгі бөлімге оралу ↩️')
        keyboard.insert(bakc_to_main_categories)
        await message.answer('Категориялардың бірін таңдаңыз', reply_markup=keyboard)


@dp.message_handler(text='Негізгі бөлімге оралу ↩️')
async def return_back_to_menu(message: types.Message):
    await message.answer('Бөлімдердің бірін таңдаңыз', reply_markup=category_menu)

for main_category in read_file:
    for category_ in read_file[main_category]:
        @dp.message_handler(text=category_['category_title'])
        async def select_book(message: types.Message):
            keyboards = category_returner(message.text)
            await message.answer(text='Кітапты таңдаңыз', reply_markup=keyboards)


@dp.message_handler()
async def send_book_document(message: types.Message):
    for main_category_title in read_file:
        for category_title_ in read_file[main_category_title]:
            for book in category_title_['books']:
                if message.text == book[1]:
                    response = requests.get(book[0])
                    soup = bs(response.text, 'html.parser')
                    tab_block = soup.find('div', class_='tab-block')
                    file = re.search(r'https(.*?)(epub|pdf)', str(tab_block)).group(0)
                    url = file.replace('\\', '')
                    if str(url).endswith('pdf'):
                        print("----------------sending pdf file----------------")
                        await bot.send_document(message.chat.id, document=url)
                    else:
                        print('----------------sending epub file----------------')
                        path = '/home/kanagat/PycharmProjects/Telegram bot projects/kitap_bot/media/'
                        # checking file exist or not
                        if os.path.exists(f'{path}+{message.text}.epub'):
                            await bot.send_document(
                                chat_id=message.chat.id,
                                document=open(f'{path}{message.text}.epub', 'rb')
                            )
                        else:
                            print('----------------Downloading file-----------------')
                            source = urllib.request.urlopen(url).read()
                            with open(f'{path}{message.text}.epub', 'wb') as new_file:
                                new_file.write(source)
                            await bot.send_document(
                                chat_id=message.chat.id,
                                document=open(f'{path}{message.text}.epub', 'rb')
                            )

