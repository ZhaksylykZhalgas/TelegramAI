from django.apps import AppConfig
# from telegram import Bot
# from telebot.async_telebot import AsyncTeleBot
# from telegram.ext import Updater, CommandHandler
# from django.conf import settings


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    # @staticmethod
    # def polling():
    #     bot = AsyncTeleBot(token=settings.TOKEN_BOT, parse_mode='HTML')
    #     updater = Updater(token=settings.TOKEN_BOT, use_context=True)
    #     dispatcher = updater.dispatcher
    #
    #     def start(update, context):
    #         bot.send_message("Привет! Я ваш Telegram-бот.")
    #
    #     dispatcher.add_handler(CommandHandler("start", start))
    #
    #     print("Бот запущен...")
    #     updater.start_polling()
    #     updater.idle()
