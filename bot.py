#!/usr/bin/env python
# -*- coding: utf-8 -*-
import parser
import telebot
import requests
from datetime import datetime

#будем писать логи или нет
is_logging = True
print('JUST STARTED')
#логгер
def log(message, answer):
    print("\n-------")
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \nЗапрос: '{3}' \nОтвет: '{4}'".format(message.from_user.first_name,
                                                                                  message.from_user.last_name,
                                                                                  str(message.from_user.id),
                                                                                  message.text,
                                                                                     answer))
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name)
#функция обработки входящих сообщений
@bot.message_handler(content_types=['text'])
def telemipt(message):
        if message.text:
            result = parser.finalSearch(message.text)
            summary_rate = 0
            if (type(result) == list):
                if (len(result)>=5):
                    answer = 'Формулируй запрос чётче. Результатов слишком много: ' + str(len(result));
                    bot.send_message(message.chat.id, answer)
                    if (is_logging):
                        log(message, answer)
                else:
                    for item in result:
                        #чтобы ссылка красиво выглядела
                        message_url = url + 'sendMessage' + '?chat_id=' + str(message.chat.id) + \
                                      '&text=<a href="' + item['href'] + '">' + item['name'] + '</a>&parse_mode=HTML'
                        requests.get(message_url)
                        answer = item['name']
                        if (is_logging):
                            log(message, answer)
            elif (type(result) == dict):
                for key in result:
                    if (type(result[key]) == list):
                        rateList = ''
                        for item in result[key]:
                            summary_rate += num(item['value'])
                            rateList += categories_prettify(item)
                        bot.send_message(message.chat.id, rateList)
                    elif (key == 'image'):
                            bot.send_photo(message.chat.id, 'http://wikimipt.org/' + result[key] )
                    else:
                        if (key == 'name'):
                            answer = result[key]
                            bot.send_message( message.chat.id, result[key] )
                if (is_logging):
                    log(message, answer)
            else:
                bot.send_message(message.chat.id, 'Ничего не найдено')
                answer = 'Ничего не найдено'
                if (is_logging):
                    log(message, answer)    
           
            if (summary_rate != 0):
                bot.send_message( message.chat.id, make_bot_prediction( summary_rate / 5 )) 
           
                
#берет значение рейтинга(число) по данному полю 
def num(line):
    words = line.split(' ')
    num = words[0]
    if (not num.isalpha() and num != '('):  
        return float(num)
    else:
        return 0.0

def make_bot_prediction(val):
    if ( round(val) == 5 ):
        return u'Бот считает, что этот препод бог'
    elif ( round(val) == 4 ):
        return u'Бот считает, что этот препод классный'
    elif ( round(val) == 3 ):
        return u'Бот считает, что этот препод среднячок'
    elif ( round(val) == 2 ):
        return u'Бот считает, что этот препод так себе'
    return u'Бот считает, что это опасность'

#инсайт : телеграм сжимает пробелы и нижние подчеркивания и черт знает что еще - записи,
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
        return item['skill'] +  '                        ' + \
        emoji_prettify(item['value']) + '\n'
    elif (item['skill'] == u'Общая оценка'):
        return item['skill'] + '                  ' + \
        emoji_prettify(item['value']) + '\n'
    else:
        return item['skill'] + '      ' + \
        emoji_prettify(item['value']) + '\n'

#печатает звездочки для рейтинга
def emoji_prettify(line):
    return round(num(line)) * u'★' + (5 - round(num(line))) * u'☆' + '   ' + line

bot.polling(none_stop=True, interval=0);

