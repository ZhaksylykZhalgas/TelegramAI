import logging

import telebot
from django.conf import settings
from django.core.management.base import BaseCommand
import asyncio

from main.main_bot import bot

logger = logging.getLogger(__name__)

telebot.logger.setLevel(settings.LOG_LEVEL)

class Command(BaseCommand):
    help = 'Запускаем бота'

    def handle(self, *args, **options):
        try:
            asyncio.run(bot.infinity_polling(logger_level=settings.LOG_LEVEL))
        except Exception as err:
            logger.error(f'Error: {err}')
