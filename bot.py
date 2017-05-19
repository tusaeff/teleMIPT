#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import parser
import requests

#turn on/turn off logs
logging = True


def log(message, answer):
    print("\n-------")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \nЗапрос: '{3}' \nОтвет: '{4}'".format(message.from_user.first_name,
                                                                                  message.from_user.last_name,
                                                                                  str(message.from_user.id),
                                                                                  message.text,
                                                                                   answer))

@bot.message_handler(content_types=['text'])
def telemipt(message):
        if message.text:
            result = parser.finalSearch(message.text)
            rate = 0
            if (type(result) == list):
                if len(result)>=5:
                    bot.send_message(message.chat.id, 'Формулируй запрос чётче. Результатов слишком много: ' + str(len(result)))
                else:
                    for item in result:
                        message_url = url + 'sendMessage' + '?chat_id=' + str(message.chat.id) + \
                                      '&text=<a href="' + item['href'] + '">' + item['name'] + '</a>&parse_mode=HTML'
                        requests.get(message_url)
                        answer = item['name']
                        log(message, answer)
            elif (type(result) == dict):
                for key in result:
                    if (type(result[key]) == list):
                        rateList = ''
                        for item in result[key]:
                        
                            rate += num(item['value'])
                            if(item['skill'] == u'Знания'):
                                rateList = rateList + item['skill'] + '                                ' + \
                                           emojiPrettify(item['value']) + '\n'
                            elif (item['skill'] == u'В общении'):
                                rateList = rateList + item['skill'] + '                         ' + \
                                           emojiPrettify(item['value']) + '\n'
                            elif (item['skill'] == u'Халявность'):
                              rateList = rateList + item['skill'] +  '                        ' + \
                                          emojiPrettify(item['value']) + '\n'
                            elif (item['skill'] == u'Общая оценка'):
                                rateList = rateList + item['skill'] + '                  ' + \
                                           emojiPrettify(item['value']) + '\n'
                            else:
                                rateList= rateList + item['skill'] + '      ' + \
                                          emojiPrettify(item['value']) + '\n'
                        bot.send_message(message.chat.id, rateList)
                    elif (key == 'image'):
                            bot.send_photo(message.chat.id, 'http://wikimipt.org/' + result[key] )
                    else:
                        if (key == 'name'):
                            answer = result[key]
                            bot.send_message(message.chat.id, result[key] )
                            if logging == True:
                                log(message, answer)
            else:
                bot.send_message(message.chat.id, 'Ничего не найдено')
            if (rate / 5 >= 4.5 and rate!=0) :
                bot.send_message(message.chat.id, 'Бот считает, что этот препод бог')
            elif (rate / 5 >= 4 and rate / 5 < 4.5 and rate != 0):
                bot.send_message(message.chat.id, 'Бот считает, что этот препод классный')
            elif (rate / 5 >= 3 and rate / 5 < 4 and rate!=0):
                bot.send_message(message.chat.id, 'Бот считает, что этот препод среднячок')
            elif (rate / 5 >= 2 and rate / 5 < 3 and rate != 0):
                bot.send_message(message.chat.id, 'Бот считает, что этот препод так себе')
            elif (rate!=0):
                bot.send_message(message.chat.id, 'Бот считает, что это опасность')

#думаю здесь надо прописать, что если там надпись (нет оценок) то значение выставить 0
# и когда будем выводить оценки делать проверку на то, что значение 0->пишем нет оценок
def num(line):
    words = line.split(' ')
    num = words[0]
    if (not num.isalpha() and num != '('):  
        print(num)
        return float(num)
    else:
        print(num + ' false ')
        return 0.0

def emojiPrettify(line):
    return emojify(num(line)) + '   ' + line

def emojify(num):
    if(num >= 4.5):
        return u'★★★★★'
    if round(num) == 4 :
        return u'★★★★☆'
    elif round(num) == 3 :
        return u'★★★☆☆'
    elif round(num) == 2 :
        return u'★★☆☆☆'
    elif round(num) == 1 :
        return u'★☆☆☆☆'
    return u'☆☆☆☆☆'

# def emojify(num):
#     if(num >= 4.5):
#         return u'❤️❤️❤️❤️❤️'
#     if num // 1 == 4 :
#         return u'⭐️⭐️⭐️⭐️       '
#     elif num//1 == 3 :
#         return u'⭐️⭐️⭐             '
#     elif num//1 == 2 :
#         return u'🍆🍆                    '
#     return u'🆘                           '

# @bot.message_handler(commands=['start'])
# def keyboard(message):
#     user_markup = telebot.types.ReplyKeyboardMarkup(True)
#     user_markup.row('/start')
#     bot.send_message(message.from_user.id, 'здрасте', reply_markup=user_markup)

bot.polling(none_stop=True, interval=0)

