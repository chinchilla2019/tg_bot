from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from db import Database
import markups as mu
import requests
from apikey import APIKEY, OPENAIKEY

bot = Bot(token=APIKEY)
dp = Dispatcher(bot)
not_ai = False
data = Database('database.db')


# устанавливаем комманды
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not data.user_exists(message.from_user.id):
        data.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, f"Здравствуйте,"
                                                     f" {message.from_user.username}! Укажите Ваш ник, "
                                                     f"он должен быть не более 20 символов. Среди символов"
                                                     f" также не должно быть пробелов, знаков @ и /")
    else:
        await bot.send_message(message.from_user.id, "Вы уже зарегистрированы")


@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    await bot.send_message(message.from_user.id, 'Используйте кнопку "как задать вопрос", '
                                                 'чтобы научиться правильно задавать вопросы. '
                                                 'Ответ приходит в сренем в течении 2-3 минут, так как происходит '
                                                 'соединение с сервером и получение ответа от нейросети')


@dp.message_handler(commands=['setname'])
async def setname(message: types.Message):
    global not_ai
    not_ai = True
    await bot.send_message(message.from_user.id, "Укажите Ваш новый ник")


# ловим изображения
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def bot_image(message: types.Message):
    await bot.send_photo(message.from_user.id, photo=message.photo[-1].file_id)


# ловим сообщения
@dp.message_handler()
async def bot_message(message: types.Message):
    global not_ai
    if message.chat.type == 'private':
        # сообщения кнопок
        if message.text == 'Что такое GPT3?':
            await bot.send_message(message.from_user.id, "GPT (Generative Pre-trained Transformer)"
                                                         " - это класс алгоритмов глубокого "
                                                         "обучения для генерации текста,"
                                                         " ответов на вопросы и выполнения других задач "
                                                         "обработки естественного языка. "
                                                         "GPT широко используется в различных "
                                                         "задачах таких как автоматическое"
                                                         " написание статей и текстов, "
                                                         "рекомендательные системы, "
                                                         "машинный перевод и другие задачи "
                                                         "обработки естественного языка", reply_markup=mu.main_Menu)
        elif message.text == 'Описание':
            await bot.send_message(message.from_user.id, "Перед Вами бот, созданный для более"
                                                         " доступного взаимодействия с "
                                                         "GPT3, у бота есть несколько комманд "
                                                         "для взаимодействия с ним:\n"
                                                         "1) /start - запуск бота, он записывает "
                                                         "Вас в базу данных\n"
                                                         "2) /help - возможная помощь в случае неполадок\n"
                                                         "3) /setname - установка имени(отличного от имени "
                                                         "в тг), по которому к Вам можно обращаться\nТакже"
                                                         " если Вы попытаетесь отправить картинку, "
                                                         "бот пришлёт её обратно",
                                   reply_markup=mu.main_Menu)
        elif message.text == 'Как задать вопрос?':
            await bot.send_message(message.from_user.id, "Задавать вопрос лучше конкретно, причем текст "
                                                         "вопроса не должен совпадать с названиями кнопок."
                                                         " Никаких особых действий выполнять не нужно,"
                                                         " также бот не отвечает на вопрос по картинке, "
                                                         "печатаем лапками)",
                                   reply_markup=mu.main_Menu)
        else:
            if data.get_signup(message.from_user.id) == "setnickname" or not_ai:
                if len(message.text) > 20:
                    await bot.send_message(message.from_user.id,
                                           "Максимальная длина названия Вашего профиля - 20 символов",
                                           reply_markup=mu.main_Menu)
                elif '@' in message.text or '/' in message.text or ' ' in message.text:
                    await bot.send_message(message.from_user.id, "Среди символов "
                                                                 "названия профиля не "
                                                                 "должно быть пробелов, знаков @ и /",
                                           reply_markup=mu.main_Menu)
                else:
                    data.set_user_name(message.from_user.id, message.text)
                    data.set_signup(message.from_user.id, "done")
                    not_ai = False
                    await bot.send_message(message.from_user.id,
                                           f"Поздравляю с успешной регистрацией, "
                                           f"{data.get_user_name(message.from_user.id)}!",
                                           reply_markup=mu.main_Menu)
            else:
                # сообщения для ответа chatgpt
                url = 'https://api.openai.com/v1/chat/completions'
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': OPENAIKEY
                }

                params = {
                    'model': 'gpt-3.5-turbo',
                    'messages': [{'role': 'user', 'content': message.text}]
                }

                response = requests.post(url, headers=headers, json=params)
                a = True
                answ = ''
                while a:
                    try:
                        answ = response.json()['choices'][0]['message']['content']
                        a = False
                    except KeyError:
                        a = True
                await bot.send_message(message.from_user.id, answ, reply_markup=mu.main_Menu)


executor.start_polling(dp, skip_updates=True)
