from django.apps import AppConfig
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from django.conf import settings


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    @staticmethod
    def polling():
        bot = Bot(token=settings.TOKEN_BOT)
        updater = Updater(token=settings.TOKEN_BOT, use_context=True)
        dispatcher = updater.dispatcher

        def start(update, context):
            update.message.reply_text("Привет! Я ваш Telegram-бот.")

        dispatcher.add_handler(CommandHandler("start", start))

        print("Бот запущен...")
        updater.start_polling()
        updater.idle()
