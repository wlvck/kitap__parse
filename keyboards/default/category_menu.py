import json
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

path = '/home/kanagat/PycharmProjects/Telegram bot projects/kitap_bot/data/result.json'

with open(path, 'r', encoding='utf-8') as file:
    read_file = json.load(file)
category_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

for main_category in read_file:
    menu = KeyboardButton(main_category.strip())
    category_menu.insert(menu)


def category_returner(message_text: str):
    keyboards = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for main_menu in read_file:
        for categories in read_file[main_menu]:
            if categories['category_title'] == message_text:
                for book in categories['books']:
                    buttons = KeyboardButton(text=book[1])
                    keyboards.insert(buttons)
    return keyboards
# keyboards = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
# for main_menu in read_file:
#     for categories in read_file[main_menu]:
#         if categories['category_title'] == '{}':
#             for book in categories['books']:
#                 buttons = KeyboardButton(text=book[1])
#                 keyboards.insert(buttons)
# keyboards.insert(KeyboardButton('Категорияларға оралу ↩'))
