from django.core.management.base import BaseCommand
from main.apps import *
import asyncio


class Command(BaseCommand):
    help = 'Запускаем бота'

    def handle(self, *args, **options):
        asyncio.run(BotConfig.polling())
