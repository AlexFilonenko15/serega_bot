import telebot 
import schedule
import time 
import threading
import os
from dotenv import load_dotenv


load_dotenv()
bot = telebot.TeleBot(os.environ["BOT_TOKEN"])


TG_CHAT_ID = []

def send_poll():
    if TG_CHAT_ID is not None:
        for id in TG_CHAT_ID:
            bot.send_poll(
            chat_id=id,
            question='Будеш цієї неділі?',
            options=['Так','Hi'],
            is_anonymous=False 
        )



@bot.message_handler(commands=['startpoll'])
def start_poll(message):
    global TG_CHAT_ID
    if message.chat.id not in TG_CHAT_ID:
        TG_CHAT_ID.append(message.chat.id)
    bot.send_message(message.chat.id, 'Щотижневе опитування налаштовано.')



def scheduler():
    schedule.every(1).minutes.do(send_poll)

    while True:
        schedule.run_pending()
        time.sleep(1)



threading.Thread(target=scheduler, daemon=True).start()








bot.polling(none_stop=True)