import telebot 
import os
from dotenv import load_dotenv
from telebot import types
import requests
import json
from flask import Flask, request


load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello👋\nI can help you with following crypto_coins💵\nSend command /get_values,\nif you want check prices about crypto_coins🤑\nAll information taken from BINANCE💰', parse_mode='html')

@bot.message_handler(commands=['get_values'])
def get_values(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('BTC', callback_data='BTC')
    btn2 = types.InlineKeyboardButton('ETH', callback_data='ETH')
    btn3 = types.InlineKeyboardButton('Other', callback_data='Other')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Choose what interests you:', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback:True)
def callback(call):
    if call.data != 'Other':
        coin = call.data
        value = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT')
        res = json.loads(value.text)
        price = float(res['price'])
        bot.send_message(call.message.chat.id, f'Curently price of {coin}: <b><u>{price}$</u></b>', parse_mode='html')
    else:
        bot.send_message(call.message.chat.id, 'Okay, write crypto what you need,like(BTC,ETH)')
        bot.register_next_step_handler(call.message, other)


def other(message):
    coin = message.text.upper()
    value = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT')
    if value.status_code == 200:
        res = json.loads(value.text)
        price = float(res['price'])
        bot.send_message(message.chat.id, f'Curently price of {coin}: <b><u>{price}$</u></b>', parse_mode='html')
        bot.send_message(message.chat.id, 'Do you want try one more?(Yes/No)')
        bot.register_next_step_handler(message, answer)
    else:
        bot.send_message(message.chat.id, 'You entered something incorrectly, please try again:')
        bot.register_next_step_handler(message, other)



def answer(message):
    if message.text.lower() == 'yes':
        bot.send_message(message.chat.id, 'Okay, write crypto what you need,like(BTC,ETH)')
        bot.register_next_step_handler(message, other)
    else:
        bot.send_message(message.chat.id, "Okay, I'll wait for your next command.")



@server.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def index():
    return "Bot is running", 200


if __name__ == "__main__":
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


