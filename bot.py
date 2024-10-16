import os
import logging
from logging.handlers import RotatingFileHandler

import requests

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler

from dotenv import load_dotenv

from deutche_parse import parse_resault

load_dotenv()

token = os.getenv('TOKEN')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('my_logger.log', maxBytes=5000000, backupCount=5)
logger.addHandler(handler)  

def message_format():
    message_lst = []
    for i in parse_resault():
        message = f"""
        {i['link']},
        
        city: {i['city']}
        type: {i['type']}, 
        price:{i['price']}, 
        general characteristics: {i['char']},
        address: {i['address']},
        """
        message_lst.append(message)
    print(message_lst)
    return message_lst

message_lst = message_format()

def full_parse_list(update, context):
    chat = update.effective_chat
    for message in message_lst:
        context.bot.send_message(
            chat.id,
            message,
        )

def wake_up(update, context):
    chat = update.effective_chat
    name = chat.first_name
    button = ReplyKeyboardMarkup([['/full']],resize_keyboard=True)
    
    if 'MonkeyMan' in name:
        context.bot.send_message(
            chat_id=chat.id, 
            text=f'Спасибо, что включили меня Роман пидорасов',
            )
    else:    
        context.bot.send_message(
            chat_id=chat.id, 
            text=f'Спасибо, что включили меня {name}',
            )
    
    context.bot.send_message(
        chat_id = chat.id,
        text=f'Отправь команду /parselist или жми на кнопку',
        reply_markup=button,
        )

def main():
    updater = Updater(token=token)
    updater.dispatcher.add_handler(CommandHandler('full', full_parse_list))
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))

    updater.start_polling()
    updater.idle() 

if __name__ == '__main__':
    main()