from django.core.management.base import BaseCommand
import asyncio

from main.main_bot import bot


class Command(BaseCommand):
    help = 'Запускаем бота'

    def handle(self, *args, **options):
        asyncio.run(bot.polling())
