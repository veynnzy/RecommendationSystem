import telebot
from telebot import types

bot = telebot.TeleBot('6186283547:AAECDm3XSpYUoMXwXm0xoLgXW7A7rWl9o50')

button_yes = types.KeyboardButton(text="Да")
button_no = types.KeyboardButton(text="Нет")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Введите описание фильма')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    film_desc = message.text.lower()
    global artist
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_desc = types.KeyboardButton(text="Узнать описание фильма")
    button_raiting = types.KeyboardButton(text="Узнать рейтинг фильма")
    keyboard.add(button_desc, button_raiting)
    msg = bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=keyboard)
    bot.register_next_step_handler(msg, menu)


def menu(message):
    if message.text.lower() == 'топ песен':
        msg = bot.send_message(message.from_user.id, 'Введите необходимое количество песен')
        bot.register_next_step_handler(msg, top_songs)
    elif message.text.lower() == 'текст песни':
        msg = bot.send_message(message.from_user.id, 'Введите название песни')
        bot.register_next_step_handler(msg, get_lyrics_song)


def top_songs(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(button_yes, button_no)
    msg = bot.send_message(message.from_user.id, "Исполнитель тот же или поменять?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, end)


def get_lyrics_song(message):
    song_name = message.text.lower()
    song = artist.song(song_name)
    bot.send_message(message.from_user.id, song.lyrics)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(button_yes, button_no)
    msg = bot.send_message(message.from_user.id, "Исполнитель тот же или поменять?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, end)


def end(message):
    if message.text.lower() == 'да':
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_top = types.KeyboardButton(text="Топ песен")
        button_song = types.KeyboardButton(text="Текст песни")
        keyboard.add(button_top, button_song)
        msg = bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=keyboard)
        bot.register_next_step_handler(msg, menu)
    elif message.text.lower() == 'нет':
        msg = bot.send_message(message.from_user.id, 'Введите имя исполнителя')
        bot.register_next_step_handler(msg, get_text_messages)


bot.polling(none_stop=True)
