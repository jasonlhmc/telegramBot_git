# pip install python-telegram-bot --upgrade
import os
import time

from selenium.webdriver import DesiredCapabilities
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackQueryHandler

import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import logging

import json
import base64
import re

import pymongo as pymongo
# from pypi import dnspython
from bson.json_util import dumps, loads


client = pymongo.MongoClient('')    #<--'mongodb+srv://.......'url
db = client.test
mydb = client['']   #<--collection name
mycol = mydb['']    #<--database name


TOKEN = ''  #<--Telegram bot token
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome. ' + update.effective_chat.first_name + '.')


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


def notes_txt(update, context):
    button_list = []
    for x in mycol.find({'isPaint': False}, {'title': True, 'dateStr': True, 'isPaint': True, '_id': False}):
        json_data = dumps(x)
        note_title = '[📝] ' + json.loads(json_data)['title']
        note_date_str = json.loads(json_data)['dateStr']
        button_list.append([InlineKeyboardButton(text=note_title, callback_data=('note|'+note_date_str))])
    reply_keyboard = InlineKeyboardMarkup(button_list)
    update.message.reply_text('Text notes listed below: ', reply_markup=reply_keyboard)


dispatcher.add_handler(CommandHandler('notes_txt', notes_txt))


def notes_pnt(update, context):
    button_list = []
    for x in mycol.find({'isPaint': True}, {'title': True, 'dateStr': True, 'isPaint': True, '_id': False}):
        json_data = dumps(x)
        note_title = '[🎨] ' + json.loads(json_data)['title']
        note_date_str = json.loads(json_data)['dateStr']
        button_list.append([InlineKeyboardButton(text=note_title, callback_data=('note|'+note_date_str))])
    reply_keyboard = InlineKeyboardMarkup(button_list)
    update.message.reply_text('Paint notes listed below: ', reply_markup=reply_keyboard)


dispatcher.add_handler(CommandHandler('notes_pnt', notes_pnt))


def notes_tsk(update, context):
    button_list = []
    for x in mycol.find({'isTask': True}, {'title': True, 'dateStr': True, 'isPaint': True, '_id': False}):
        json_data = dumps(x)
        note_title = '[📝] ' + json.loads(json_data)['title']
        note_date_str = json.loads(json_data)['dateStr']
        button_list.append([InlineKeyboardButton(text=note_title, callback_data=('note|'+note_date_str))])
    reply_keyboard = InlineKeyboardMarkup(button_list)
    update.message.reply_text('Task notes listed below: ', reply_markup=reply_keyboard)


dispatcher.add_handler(CommandHandler('notes_tsk', notes_tsk))


def notes_unlock(update, context):
    button_list = []
    for x in mycol.find({"$or": [{'isFPLock': True}, {'isPinLock': True}]},
                        {'title': True, 'dateStr': True, 'isPaint': True, 'isFPLock': True, 'isPinLock': True, '_id': False}):
        json_data = dumps(x)
        if bool(json.loads(json_data)['isFPLock']):
            note_title = '[🔒: 👆] ' + json.loads(json_data)['title']
        if bool(json.loads(json_data)['isPinLock']):
            note_title = '[🔒: 🔢] ' + json.loads(json_data)['title']
        if bool(json.loads(json_data)['isFPLock']) and bool(json.loads(json_data)['isPinLock']):
            note_title = '[🔒: 🔢+👆] ' + json.loads(json_data)['title']
        note_date_str = json.loads(json_data)['dateStr']
        button_list.append([InlineKeyboardButton(text=note_title, callback_data=('note_unlock|'+note_date_str))])
    reply_keyboard = InlineKeyboardMarkup(button_list)
    update.message.reply_text('Task notes listed below: ', reply_markup=reply_keyboard)


dispatcher.add_handler(CommandHandler('notes_unlock', notes_unlock))


def check_cur(update, context: CallbackContext):
    request = requests.get('https://tw.rter.info/capi.php')
    currency = request.json()
    usd_rate = float(dict(currency).get('USDHKD')['Exrate'])
    request.close()
    usd = '\U0001F1FA\U0001F1F8 -> \U0001F1ED\U0001F1F0 = ' + str(round(usd_rate, 3))
    gbp = '\U0001F1EC\U0001F1E7 -> \U0001F1ED\U0001F1F0 = ' + str(
        round(usd_rate / float(dict(currency).get('USDGBP')['Exrate']), 3))
    vnd = '\U0001F1ED\U0001F1F0 -> \U0001F1FB\U0001F1F3 = ' + str(
        round(float(dict(currency).get('USDVND')['Exrate']) / usd_rate, 3))
    myr = '\U0001F1ED\U0001F1F0 -> \U0001F1F2\U0001F1FE = ' + str(
        round(float(dict(currency).get('USDMYR')['Exrate']) / usd_rate, 3))
    thb = '\U0001F1ED\U0001F1F0 -> \U0001F1F9\U0001F1ED = ' + str(
        round(float(dict(currency).get('USDTHB')['Exrate']) / usd_rate, 3))
    rs = usd + "\r\n" + gbp + "\r\n" + vnd + "\r\n" + myr + "\r\n" + thb
    context.bot.send_message(update.effective_chat.id, rs)


dispatcher.add_handler(CommandHandler('check_cur', check_cur))


def dl(update, context: CallbackContext):
    try:
        context.bot.send_message(update.effective_chat.id, 'Downloader initializing...')
        options = Options()
        options.add_experimental_option('w3c', False)
        options.add_argument("--headless")
        cap = DesiredCapabilities.CHROME
        cap["goog:loggingPrefs"] = {"performance": "ALL"}
        driver_path = ''    #<--Chromedriver loaction, check: https://chromedriver.chromium.org/downloads
        driver = webdriver.Chrome(executable_path=driver_path, options=options, desired_capabilities=cap)
        driver.get(context.args[0])
        video_title = driver.find_element_by_css_selector(
            '#span-1160 > div.span-real-985.right > div.span-640.left > h1').get_attribute('innerHTML')
        context.bot.send_message(update.effective_chat.id, '「' + video_title + '」 Found. Processing..')
        process_time = time.time()
        log = driver.get_log("performance")
        video_url_list = re.findall(
            # "(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
            '"https://.*?"'
            , str(log))
        driver.close()
        dl_link = ''
        for video_url in video_url_list:
            if 'dashinit.mp4' in video_url:
                dl_link = video_url.replace('"', '')
                break
        # convert title to file name
        output_file_name = ''
        format_str_list = re.findall('/[^A-Za-z\u4E00-\u9FFF]/ug', str(video_title))
        if format_str_list:
            output_file_name = str(format_str_list)
            for format_str in re.findall('/[^A-Za-z\u4E00-\u9FFF]/ug', str(video_title)):
                output_file_name = output_file_name.replace(format_str, '')
        else:
            output_file_name = str(video_title).replace(' ', '')
        output = output_file_name + '.mp4'
        if not os.path.isfile(output):
            context.bot.send_message(update.effective_chat.id, '「' + output + '」 Download Started..')
            try:
                r = requests.get(dl_link, allow_redirects=True)
                open(output, 'ab').write(r.content)
            except Exception as e:
                print(e)
            r.close()
            video_size_byte = os.path.getsize(output)
            video_size_mb = video_size_byte / 1024 / 1024
            if video_size_byte < 52428800:
                context.bot.sendMessage(update.effective_chat.id, str(int(video_size_mb)) + 'MB Downloaded. Start Sending..')
                context.bot.sendVideo(update.effective_chat.id, open(output, 'rb'), timeout=65536)
                context.bot.sendMessage(update.effective_chat.id, 'Done in ' + str((time.time() - process_time).__int__()) + ' second(s).')
            else:
                context.bot.sendMessage(update.effective_chat.id, str(int(video_size_mb)) + 'MB Downloaded. ' +
                                '\r\nCannot send when file size over 50MB.' +
                                '\r\nSaved to local.')
                context.bot.sendMessage(update.effective_chat.id, 'Done in ' + str((time.time() - process_time).__int__()) + ' second(s).')
        else:
            context.bot.send_message(update.effective_chat.id, '「' + output + '」 Already Exist..')
            video_size_byte = os.path.getsize(output)
            video_size_mb = video_size_byte / 1024 / 1024
            if video_size_byte < 52428800:
                context.bot.sendMessage(update.effective_chat.id, str(int(video_size_mb)) + 'MB. Start Sending..')
                context.bot.sendVideo(update.effective_chat.id, open(output, 'rb'), timeout=65536)
                context.bot.sendMessage(update.effective_chat.id, 'Done in ' + str((time.time() - process_time).__int__()) + ' second(s).')
            else:
                context.bot.sendMessage(update.effective_chat.id, str(int(video_size_mb)) + 'MB. ' +
                                '\r\nCannot send when file size over 50MB.' +
                                '\r\nSaved to local.')
                context.bot.sendMessage(update.effective_chat.id, 'Done in ' + str((time.time() - process_time).__int__()) + ' second(s).')
    except Exception as e:
        context.bot.send_message.sendMessage(update.effective_chat.id, 'Error: ' + str(e))


dispatcher.add_handler(CommandHandler('dl', dl, pass_args=True))


def call_back_handle(update: Update, context: CallbackContext):
    # print(update.callback_query.data)
    call_back_type, call_back_data = update.callback_query.data.split('|')
    if call_back_type == 'note':
        rs = ''
        json_data = dumps(mycol.find_one({'dateStr': call_back_data}, {'_id': False}))
        rs += 'Note Title: ' + json.loads(json_data)['title'] + '\r\n'
        rs += 'Create Date: ' + json.loads(json_data)['dateStr'] + '\r\n'
        try:
            rs += 'Last Edit Date: ' + json.loads(json_data)['editDateStr'] + '\r\n'
        except Exception as e:
            rs += 'Last Edit Date: \r\n'
            print(e)
        if bool(json.loads(json_data)['isPaint']):
            rs += '--------------------------------------------------' + '\r\n'
            update.callback_query.edit_message_text(rs)
            decode_str_to_image(json.loads(json_data)['content'])
            context.bot.send_photo(update.effective_chat.id, open('image.png', 'rb'))
        else:
            rs += '--------------------------------------------------' + '\r\n'
            rs += json.loads(json_data)['content'] + '\r\n'
            try:
                if bool(json.loads(json_data)['isTask']):
                    task_list = json.loads(json_data)['taskList']
                    for task in task_list:
                        if task['isFinished']:
                            rs += '⭕' + task['task'] + '\r\n'
                        else:
                            rs += '❌' + task['task'] + '\r\n'
            except Exception as e:
                print(e)
            update.callback_query.edit_message_text(rs)

    if call_back_type == 'note_unlock':
        key = {"dateStr": call_back_data}
        update_val = {"$set": {"isFPLock": False, "isPinLock": False, "encryptedPin": ""}}
        mycol.update_one(key, update_val)
        updated_date = json.loads(dumps(mycol.find_one({'dateStr': call_back_data}, {'_id': False})))
        update.callback_query.edit_message_text('Note Updated. Result below: ')
        context.bot.send_message(update.effective_chat.id, json.dumps(updated_date, indent=2))


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

