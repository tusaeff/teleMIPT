#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import parser
import requests

#turn on/turn off logs
logging = True

#function send logs
def log(message, answer):
    print("\n-------")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \nЗапрос: '{3}' \nОтвет: '{4}'".format(message.from_user.first_name,
                                                                                  message.from_user.last_name,
                                                                                  str(message.from_user.id),
                                                                                  message.text,
                                                                                   answer))
#main function to send answer to the user
@bot.message_handler(content_types=['text'])
def telemipt(message):
        print('JUST STARTED')
        if message.text:
            result = parser.finalSearch(message.text)
            rate = 0
            if (type(result) == list):
                if len(result)>=5:
                    bot.send_message(message.chat.id, 'Формулируй запрос чётче. Результатов слишком много: ' + str(len(result)))
                else:
                    for item in result:
                        #чтобы ссылка красиво выглядела
                        message_url = url + 'sendMessage' + '?chat_id=' + str(message.chat.id) + \
                                      '&text=<a href="' + item['href'] + '">' + item['name'] + '</a>&parse_mode=HTML'
                        requests.get(message_url)
                        answer = item['name']
                        if logging == True:
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
                answer = 'Ничего не найдено'
                if logging == True:
                    log(message, answer)
                #variable 'rate' stores the sum of all values from the teacher's rating
                #rate/5 = average value of the teacher
                #bot makes a subjective opinion about the teacher based on this value 
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
                
#берет значение рейтинга(число) по данному полю 
def num(line):
    words = line.split(' ')
    num = words[0]
    if (not num.isalpha() and num != '('):  
        return float(num)
    else:
        return 0.0

#печатает звездочки для рейтинга
def emojiPrettify(line):
    return round(num(line)) * u'★' + (5 - round(num(line))) * u'☆' + '   ' + line

bot.polling(none_stop=True, interval=59);

