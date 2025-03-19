from telebot.async_telebot import AsyncTeleBot
from django.conf import settings
import logging

bot = AsyncTeleBot(settings.TOKEN_BOT, parse_mode='HTML')

logger = logging.getLogger(__name__)


@bot.chat_member_handler()
async def chat_member_handler_bot(message):
    status = message.difference.get('status')
    full_name = message.from_user.full_name
    invite_link = message.invite_link
    invite_link_name = ''
    invite_link_url = ''
    username = message.from_user.username
    id = message.from_user.id

    try:
        invite_link_name = getattr(invite_link, 'name')
        invite_link_url = getattr(invite_link, 'url')
    except AttributeError as err:
        logger.info(f'Not a valid invite link: {err}')

    current_subscribe_status = status[1]
    if current_subscribe_status == 'member':
        status_text = 'Subscribed'
    elif current_subscribe_status == 'left':
        status_text = 'Unsubscribed'
    else:
        status_text = 'Unknown'

    text_message = (f'{status_text}\n'
                    f'Name: {full_name}\n'
                    f'ID: {id}')
    if username:
        text_message += f'\nUsername: {username}\n'
    if invite_link_name:
        text_message += f'\nInvite name: @{invite_link_name}\n'
    if invite_link_url:
        text_message += f'\nInvite URL: {invite_link_url}\n'
    await bot.send_message(message.chat.id, text_message)


@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    await bot.send_message(message.chat.id, """\n Hi my name is Zhalgas, I am learning to create AI bot on telegram.""")



@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)
