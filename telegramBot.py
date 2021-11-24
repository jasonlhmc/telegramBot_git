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

from subprocess import Popen
import glob

import cv2
import pytesseract

import torch
import torchvision
import numpy as np
import argparse
from PIL import Image
from torchvision.transforms import transforms as transforms

import matplotlib

edges = [
    (0, 1), (0, 2), (2, 4), (1, 3), (6, 8), (8, 10),
    (5, 7), (7, 9), (5, 11), (11, 13), (13, 15), (6, 12),
    (12, 14), (14, 16), (5, 6)
]

client = pymongo.MongoClient('')    #<--'mongodb+srv://.......'url
db = client.test
mydb = client['']   #<--collection name
mycol = mydb['']    #<--database name

LIBRE_OFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

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


def docx_pdf_convert(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    file_name = update.message.document.file_name
    docx = context.bot.get_file(update.message.document).download(file_name)

    if docx.endswith('.docx'):
        process_time = time.time()
        context.bot.sendMessage(chat_id, 'Its docx; ' + file_name)
        context.bot.sendMessage(chat_id, 'Start converting docx to pdf..')
        converted_file = file_name.replace('.docx', '.pdf')
        convert_to_pdf(file_name, '')
        if os.path.isfile(converted_file):
            context.bot.send_document(chat_id, open(converted_file, 'rb'))
            context.bot.sendMessage(chat_id, 'Done in ' + str((time.time() - process_time).__int__()) + ' second(s).')
    else:
        context.bot.sendMessage(chat_id, 'Not docx; ' + file_name)


dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.document, docx_pdf_convert))


def get_text_from_image(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    image_in = context.bot.get_file(update.message.photo[-1].file_id).download('image_in.png')
    caption = update.message.caption

    image_cv2 = cv2.imread(image_in)
    image_cv2 = cv2.resize(image_cv2, None, fx=2, fy=2)
    image_cv2 = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)
    image_cv2 = cv2.threshold(image_cv2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imwrite('cv2_image.png', image_cv2)

    if caption in pytesseract.get_languages(config='') or caption == 'all':
        print('Lang arg found.')
        process_time = time.time()
        context.bot.sendMessage(chat_id, 'Start getting text from image..')
        if caption == 'all':
            lang_all = ''
            i = 0
            for tesseract_lang in pytesseract.get_languages(config=''):
                i += 1
                if i == pytesseract.get_languages(config='').__len__():
                    lang_all += tesseract_lang
                else:
                    lang_all += tesseract_lang + '+'
            rs = pytesseract.image_to_string('cv2_image.png', lang=lang_all, config='--psm 6')
        else:
            rs = pytesseract.image_to_string('cv2_image.png', lang=caption, config='--psm 6')
        context.bot.sendMessage(chat_id, rs)
        context.bot.sendMessage(chat_id, 'Done in ' + str((time.time() - process_time).__int__()) + ' second(s).')
    else:
        print('No lang arg found.')
        button_list = []
        for tesseract_lang in pytesseract.get_languages(config=''):
            button_list.append([InlineKeyboardButton(text=tesseract_lang, callback_data='image_text' + '|' + tesseract_lang)])
        button_list.append([InlineKeyboardButton(text='all', callback_data='image_text' + '|' + 'all')])
        button_list.append([InlineKeyboardButton(text='rcnn', callback_data='rcnn' + '|' + image_in)])
        reply_keyboard = InlineKeyboardMarkup(button_list)
        update.message.reply_text('Select Language: ', reply_markup=reply_keyboard)


dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.photo, get_text_from_image))


def delete_file(update, context: CallbackContext):
    file_list = []
    long_file_name = ""
    print("len(context.args) = " + str(len(context.args)))
    if len(context.args) == 0:
        for file_name in glob.glob(os.getcwd() + "/*"):
            if not file_name.endswith(".py") and os.path.isfile(file_name):
                fn = file_name.replace(os.getcwd(), "")
                if len(fn.encode('utf-8')) > (64 - len('delete_file' + '|')):
                    long_file_name += fn + "\r\n"
                else:
                    file_list.append([InlineKeyboardButton(text=fn, callback_data='delete_file' + '|' + fn)])
        file_list.append([InlineKeyboardButton(text='❌EXIT❌', callback_data='delete_file' + '|' + 'exit')])
        reply_keyboard = InlineKeyboardMarkup(file_list)
        update.message.reply_text('Select file to remove: ', reply_markup=reply_keyboard)
        if long_file_name != "":
            context.bot.sendMessage(update.effective_chat.id, "Files cannot delete: \r\n" + long_file_name)
    else:
        context.bot.sendMessage(update.effective_chat.id, "No arg needed.")


dispatcher.add_handler(CommandHandler('delete_file', delete_file))


def call_back_handle(update: Update, context: CallbackContext):
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
            context.bot.send_photo(update.effective_chat.id, open('note_paint.png', 'rb'))
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

    if call_back_type == 'image_text':
        process_time = time.time()
        arg = call_back_data
        if arg == 'all':
            lang_all = ''
            i = 0
            for tesseract_lang in pytesseract.get_languages(config=''):
                i += 1
                if i == pytesseract.get_languages(config='').__len__():
                    lang_all += tesseract_lang
                else:
                    lang_all += tesseract_lang + '+'
            update.callback_query.edit_message_text(lang_all)
            context.bot.sendMessage(update.effective_chat.id, 'Start getting text from image..')
            rs = pytesseract.image_to_string('cv2_image.png', lang=lang_all, config='--psm 6')
        else:
            update.callback_query.edit_message_text(arg)
            context.bot.sendMessage(update.effective_chat.id, 'Start getting text from image..')
            rs = pytesseract.image_to_string('cv2_image.png', lang=arg, config='--psm 6')
        context.bot.sendMessage(update.effective_chat.id, rs)
        context.bot.sendMessage(update.effective_chat.id, 'Done in ' + str((time.time() - process_time).__int__()) + ' second(s).')

    if call_back_type == 'rcnn':
        process_time = time.time()
        arg = call_back_data

        transform = transforms.Compose([transforms.ToTensor()])
        model = torchvision.models.detection.keypointrcnn_resnet50_fpn(pretrained=True, num_keypoints=17)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device).eval()
        image = Image.open(call_back_data).convert('RGB')
        orig_numpy = np.array(image, dtype=np.float32)
        orig_numpy = cv2.cvtColor(orig_numpy, cv2.COLOR_RGB2BGR) / 255.
        image = transform(image)
        image = image.unsqueeze(0).to(device)
        with torch.no_grad():
            outputs = model(image)
        output_image = draw_points(outputs, orig_numpy)
        cv2.waitKey(0)
        cv2.imwrite("image_out_rcnn.png", output_image * 255.)

        context.bot.send_photo(update.effective_chat.id, open("image_out_rcnn.png", 'rb'))
        update.callback_query.edit_message_text('Done in ' + str((time.time() - process_time).__int__()) + ' second(s).')

    if call_back_type == 'delete_file':
        if call_back_data == "exit":
            update.callback_query.edit_message_text("EXIT delete file process.")
        else:
            if os.path.exists(os.getcwd() + call_back_data):
                os.remove(os.getcwd() + call_back_data)
                file_list = []
                long_file_name = ""
                for file_name in glob.glob(os.getcwd() + "/*"):
                    if not file_name.endswith(".py") and os.path.isfile(file_name):
                        fn = file_name.replace(os.getcwd(), "")
                        if len(fn.encode('utf-8')) > (64 - len('delete_file' + '|')):
                            long_file_name += fn + "\r\n"
                        else:
                            file_list.append([InlineKeyboardButton(text=fn, callback_data='delete_file' + '|' + fn)])
                file_list.append([InlineKeyboardButton(text='❌EXIT❌', callback_data='delete_file' + '|' + 'exit')])
                reply_keyboard = InlineKeyboardMarkup(file_list)
                update.callback_query.edit_message_reply_markup(reply_markup=reply_keyboard)
                if long_file_name != "":
                    context.bot.sendMessage(update.effective_chat.id, "Files cannot delete: \r\n" + long_file_name)
            else:
                context.bot.sendMessage(update.effective_chat.id, "File Not Found.")


dispatcher.add_handler(CallbackQueryHandler(call_back_handle))


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Invalid command.')


dispatcher.add_handler(MessageHandler(Filters.command, unknown))


def decode_str_to_image(img_data):
    image = open("note_paint.png", "wb")
    image.write(base64.b64decode(img_data))
    image.close()
    return image


def convert_to_pdf(input_docx, out_folder):
    p = Popen([LIBRE_OFFICE, '--headless', '--convert-to', 'pdf', '--outdir',
               out_folder, input_docx])
    print([LIBRE_OFFICE, '--convert-to', 'pdf', input_docx])
    p.communicate()


def draw_points(outputs, image):
    # the `outputs` is list which in-turn contains the dictionaries
    for i in range(len(outputs[0]['keypoints'])):
        points = outputs[0]['keypoints'][i].cpu().detach().numpy()
        # proceed to draw the lines if the confidence score is above 0.9
        if outputs[0]['scores'][i] > 0.9:
            points = points[:, :].reshape(-1, 3)
            for p in range(points.shape[0]):
                # draw the keypoints
                cv2.circle(image, (int(points[p, 0]), int(points[p, 1])),
                           3, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
                # uncomment the following lines if you want to put keypoint number
                # cv2.putText(image, f"{p}", (int(keypoints[p, 0]+10), int(keypoints[p, 1]-5)),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            for ie, e in enumerate(edges):
                # get different colors for the edges
                rgb = matplotlib.colors.hsv_to_rgb([
                    ie / float(len(edges)), 1.0, 1.0
                ])
                rgb = rgb * 255
                # join the keypoint pairs to draw the skeletal structure
                cv2.line(image, (int(points[e, 0][0]), int(points[e, 1][0])),
                         (int(points[e, 0][1]), int(points[e, 1][1])),
                         tuple(rgb), 2, lineType=cv2.LINE_AA)
        else:
            continue
    return image


updater.start_polling()
updater.idle()

