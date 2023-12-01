import telebot
import dotenv


bot_token = dotenv.get_variable(".env", key="BOT_TOKEN")
bot = telebot.TeleBot(bot_token)
