import telebot

from constants import TELEGRAM_API_TOKEN, TELEGRAM_USER_ID

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)


def send_message(message):
    return bot.send_message(TELEGRAM_USER_ID, message)