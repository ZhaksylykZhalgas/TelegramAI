import os

import fitz
from docx import Document
from telebot import types
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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton('Download business plan')
    # help_button = types.KeyboardButton('Help')
    markup.add(start_button)
    await bot.send_message(message.chat.id, """\n Hi my name is Zhalgas, I am learning to create AI bot on telegram.""",
                           reply_markup=markup)


@bot.message_handler(content_types=['text'])
async def button(message):
    if message.text == 'Download business plan':
        await bot.send_message(message.chat.id, 'Ok, send me your business plan')
    else:
        await bot.send_message(message.chat.id, 'May be you should command (/help)')


@bot.message_handler(content_types=['document'])
async def read_file(message: types.Message):
    document = message.document
    file_id = document.file_id
    file_name = document.file_name

    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    local_path = f'downloads/{file_name}'

    if not file_info:
        await bot.send_message(message.chat.id, 'No file found')
        return

    try:
        downloaded_file = await bot.download_file(file_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        with open(local_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        extracted_text = ''
        if file_name.endswith('.txt'):
            extracted_text = extract_text_from_txt(local_path)
        elif file_name.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(local_path)
        elif file_name.endswith('.docx'):
            extracted_text = extract_text_from_word(local_path)
        else:
            await bot.send_message(message.chat.id, 'Supporting only PDF, WORD or TXT')
            return

        if extracted_text:
            await bot.send_message(message.chat.id, f'Extracted text:\n\n ```{extracted_text}```', parse_mode='Markdown')
        else:
            await bot.send_message(message.chat.id, 'No text extracted')

    except Exception as err:
        await bot.send_message(message.chat.id, 'Wrong while downloading file')
    finally:
        if os.path.exists(local_path):
            os.remove(local_path)

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def extract_text_from_pdf(file_path):
    text = ''
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.getText()
    return text.strip()

def extract_text_from_word(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs]).strip()

@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)
