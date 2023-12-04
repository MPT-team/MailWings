from typing import Final
import telebot



if __name__ == '__main__':
    bot = telebot.TeleBot(token=TOKEN)
    bot.send_message(CHAT_ID, 'Hi! I\'m a Bot!')
