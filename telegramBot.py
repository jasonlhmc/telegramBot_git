from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import logging

import json
import base64

import pymongo as pymongo
# from pypi import dnspython
from bson.json_util import dumps


client = pymongo.MongoClient('') #<--'mongodb+srv://.......'url
db = client.test
mydb = client[''] #<--collection name
mycol = mydb[''] #<--database name


TOKEN = '' #<--Telegram bot token
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome. /help to get command list.')


dispatcher.add_handler(CommandHandler('start', start))


def notes_all(update, context):
    button_list = []
    for x in mycol.find({}, {'title': True, 'dateStr': True, 'isPaint': True, '_id': False}):
        json_data = dumps(x)
        if bool(json.loads(json_data)['isPaint']):
            note_title = '[🎨] ' + json.loads(json_data)['title']
        else:
            note_title = '[📝] ' + json.loads(json_data)['title']
        note_date_str = json.loads(json_data)['dateStr']
        button_list.append([InlineKeyboardButton(text=note_title, callback_data=('note|'+note_date_str))])
    reply_keyboard = InlineKeyboardMarkup(button_list)
    update.message.reply_text('All notes listed below: ', reply_markup=reply_keyboard)


dispatcher.add_handler(CommandHandler('notes_all', notes_all))


def call_back_handle(update: Update, context: CallbackContext):
    # print(update.callback_query.data)
    call_back_type, call_back_data = update.callback_query.data.split('|')
    if call_back_type == 'note':
        rs = ''
        json_data = dumps(mycol.find_one({'dateStr': call_back_data}, {'_id': False}))
        rs += 'Note Title: ' + json.loads(json_data)['title'] + '\r\n'
        rs += 'Create Date: ' + json.loads(json_data)['dateStr'] + '\r\n'
        rs += 'Last Edit Date: ' + json.loads(json_data)['editDateStr'] + '\r\n'
        if bool(json.loads(json_data)['isPaint']):
            rs += '--------------------------------------------------' + '\r\n'
            update.callback_query.edit_message_text(rs)
            decode_str_to_image(json.loads(json_data)['content'])
            context.bot.send_photo(update.effective_chat.id, open('image.png', 'rb'))
        else:
            rs += '--------------------------------------------------' + '\r\n'
            rs += json.loads(json_data)['content']
            update.callback_query.edit_message_text(rs)


dispatcher.add_handler(CallbackQueryHandler(call_back_handle))


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Invalid command.')


dispatcher.add_handler(MessageHandler(Filters.command, unknown))


def decode_str_to_image(img_data):
    image = open("image.png", "wb")
    image.write(base64.b64decode(img_data))
    image.close()
    return image


updater.start_polling()
updater.idle()

