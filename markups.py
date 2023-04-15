from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bth_description = KeyboardButton('Описание')
btn_what_is_gpt = KeyboardButton('Что такое GPT3?')
btn_how_to_ask = KeyboardButton('Как задать вопрос?')
main_Menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_Menu.add(bth_description, btn_what_is_gpt, btn_how_to_ask)
