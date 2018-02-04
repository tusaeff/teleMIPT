#!/usr/bin/env python
# -*- coding: utf-8 -*-
import parser
import telebot
import requests
from datetime import datetime, date
from flask import Flask, request
import os
if (os.environ['STAGE'] != 'DEV'):
    from database import db, Prepod, Stats, server

from telebot import types
from keys import token

bot = telebot.TeleBot(token)
url = 'https://api.telegram.org/bot{0}/'.format(token)

IS_NOT_WORKING = False
IS_LOGGING = True
IS_DEVELOPMENT = os.environ['STAGE'] == 'DEV'
print('JUST STARTED')
# логгер


def log(message, answer):
    print(datetime.now())
    print(
        "Сообщение от {0} {1}. (id = {2}) \nЗапрос: '{3}' \nОтвет: '{4}'".format(
            message.from_user.first_name, message.from_user.last_name, 
                str(message.from_user.id).encode('utf-8'), message.text, answer))
    print("\n-------")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        'Привет, ' +
        message.from_user.first_name)


@bot.message_handler(
    func=lambda message: IS_NOT_WORKING,
    content_types=['text'])
def answer_when_not_work(message):
    answer = 'Кажется, викимипт не работает 🤧'
    bot.send_message(message.chat.id, answer)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def telemipt(message):
    if message.text:
        remove_markup = types.ReplyKeyboardRemove()
        bot.send_chat_action(message.chat.id, 'typing')
        result = parser.finalSearch(message.text)
        summary_rate = 0
        if (isinstance(result, list)):
            if (len(result) >= 5):
                answer = 'Формулируй запрос чётче. Результатов слишком много: ' + \
                    str(len(result))
                bot.send_message(
                    message.chat.id,
                    answer,
                    reply_markup=remove_markup)
                if (IS_LOGGING):
                    log(message, answer)
            else:
                markup = types.ReplyKeyboardMarkup(
                    row_width=1, one_time_keyboard=True)
                for item in result:
                    message_url = url + 'sendMessage' + '?chat_id=' + str(message.chat.id) + \
                        '&text=<a href="' + item['href'] + '">' + item['name'] + '</a>&parse_mode=HTML'
                    requests.get(message_url)
                    markup.add(types.KeyboardButton(item['name']))
                    answer = item['name']
                    if (IS_LOGGING):
                        log(message, answer)
                bot.send_message(
                    message.chat.id,
                    "Выберите преподавателя:",
                    reply_markup=markup)
        elif (isinstance(result, dict)):
            for key in result:
                if (isinstance(result[key], list)):
                    rateList = ''
                    for item in result[key]:
                        summary_rate += num(item['value'])
                        rateList += categories_prettify(item)
                    bot.send_message(message.chat.id, rateList)
                elif (key == 'image'):
                    bot.send_photo(
                        message.chat.id,
                        'http://wikimipt.org/' +
                        result[key])
                else:
                    if (key == 'name'):
                        answer = result[key]
                        bot.send_message(
                            message.chat.id, result[key], reply_markup=remove_markup)
            if (IS_LOGGING):
                log(message, answer)
            if (summary_rate != 0):
                bot.send_message(
                    message.chat.id,
                    make_bot_prediction(
                        summary_rate / 5))
            else:
                bot.send_message(message.chat.id, 'Here be dragons later')

            if (not IS_DEVELOPMENT):
                preps = list(Prepod.query.filter_by(name=result['name']))
                if (len(preps) == 0):
                    prep = Prepod(result['name'])
                    db.session.add(prep)
                    db.session.flush()
                else:
                    prep = preps[0]
                db.session.add(Stats(prep.id, message.chat.id))
                db.session.commit()
        else:
            bot.send_message(
                message.chat.id,
                'Ничего не найдено',
                reply_markup=remove_markup)
            answer = 'Ничего не найдено'
            if (IS_LOGGING):
                log(message, answer)


def num(line):
    '''берет значение рейтинга(число) по данному полю'''
    words = line.split(' ')
    num = words[0]
    if (not num.isalpha() and num != '('):
        return float(num)
    else:
        return 0.0


def make_bot_prediction(rate):
    ''' делаем предсказание исходя из суммарного рейтинга '''
    if (rate >= 4.5):
        return 'Бот считает, что этот препод бог'
    elif (rate >= 4 and rate < 4.5):
        return 'Бот считает, что этот препод классный'
    elif (rate >= 3 and rate < 4):
        return 'Бот считает, что этот препод среднячок'
    elif (rate >= 2 and rate < 3):
        return 'Бот считает, что этот препод так себе'
    else:
        return 'Бот считает, что это опасность'

# инсайт : телеграм сжимает пробелы и нижние подчеркивания и черт знает что еще - записи,
#         в которых одинаковое число символов могут иметь разную длину, поэтому число пробелов нельзя
#         рассчитать исходя из длины строки


def categories_prettify(item):
    if(item['skill'] == u'Знания'):
        return item['skill'] + '                                ' + \
            emoji_prettify(item['value']) + '\n'
    elif (item['skill'] == u'В общении'):
        return item['skill'] + '                         ' + \
            emoji_prettify(item['value']) + '\n'
    elif (item['skill'] == u'Халявность'):
        return item['skill'] + '                        ' + \
            emoji_prettify(item['value']) + '\n'
    elif (item['skill'] == u'Общая оценка'):
        return item['skill'] + '                  ' + \
            emoji_prettify(item['value']) + '\n'
    else:
        return item['skill'] + '      ' + \
            emoji_prettify(item['value']) + '\n'


def emoji_prettify(line):
    '''печатает звездочки для рейтинга'''
    return round(num(line)) * u'★' + \
        (5 - round(num(line))) * u'☆' + '   ' + line


if (not IS_DEVELOPMENT):
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates(
            [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200


    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://mipttelegram.herokuapp.com/bot")
        return "!", 200


    @server.route("/stop")
    def webhook_stop():
        bot.remove_webhook()


    server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
    server = Flask(__name__)

else:
    bot.polling();