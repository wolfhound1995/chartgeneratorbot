import telebot
from telebot import types
import os
from os.path import join, dirname
from dotenv import load_dotenv
def get_from_env(key):
    dotenv_path = join(dirname(__file__), 'token.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)
token = get_from_env('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    bar = types.InlineKeyboardButton("bar", callback_data="bar")
    line = types.InlineKeyboardButton("line", callback_data="line")
    radar = types.InlineKeyboardButton("radar", callback_data="radar")
    pie = types.InlineKeyboardButton("pie", callback_data="pie")
    doughnut = types.InlineKeyboardButton("doughnut", callback_data="doughnut")
    polar = types.InlineKeyboardButton("polar", callback_data="polarArea")
    scatter = types.InlineKeyboardButton("scatter", callback_data="scatter")
    bubble = types.InlineKeyboardButton("bubble", callback_data="bubble")
    radial_gauge = types.InlineKeyboardButton("radial gauge", callback_data="radialGauge")
    box_violine = types.InlineKeyboardButton("box & violine", callback_data="violin")
    sparklines = types.InlineKeyboardButton("sparklines", callback_data="sparkline")
    progress = types.InlineKeyboardButton("progress", callback_data="progressBar")
    markup.add(bar, line, radar, pie, doughnut, polar, scatter, bubble, radial_gauge, box_violine, sparklines, progress)
    bot.send_message(message.chat.id, "Choose your type of chart", reply_markup=markup)
@bot.callback_query_handler(func=lambda call: True)
def test_callback(call): # <- passes a CallbackQuery type object to your function
    user_info = {}
    user_info['graph'] = call.data
    print(call.data)
    msg = bot.send_message(call.message.chat.id, "Enter labels separated by commas. Example: \nJanuary, February, March, April, May")
    bot.register_next_step_handler(msg, graphlabels, user_info)
def graphlabels(message, user_info):
    user_info['labels'] = message.text.split(', ')
    print(user_info['labels'])
    msg = bot.send_message(message.chat.id, "Enter datasets separated by commas. Example: \nDogs, Cats")
    bot.register_next_step_handler(msg, datasets, user_info)
def datasets(message, user_info):
    user_info['datasets'] = message.text.split(', ')
    print(user_info['datasets'])
    msg = bot.send_message(message.chat.id, "Enter data for each of your datasets separated by space, count of data must = numbers of labels. Example: \n50,60,70,180,190 100,200,300,400,500")
    bot.register_next_step_handler(msg, dataforlabel, user_info)
def dataforlabel(message, user_info):
    user_info['data'] = message.text.split(' ')
    print(user_info['data'])
    graph = user_info['graph']
    labele = user_info['labels']
    dataset = user_info['datasets']
    dataforlabel = user_info['data']

    result = ''
    for f, b in zip(dataset, dataforlabel):
        arq = f"%7Blabel%3A%27{f}%27%2Cdata%3A%5B{b}%5D%7D%2C"
        print('test')
        result += arq
    messagebuilder = f"https://quickchart.io/chart?c=%7Btype%3A%27{graph}%27%2Cdata%3A%7Blabels%3A{labele}%2C%20datasets%3A%5B{result}%5D%7D%7D"
    bot.send_photo(message.chat.id, messagebuilder)
    send_welcome(message)

bot.infinity_polling()