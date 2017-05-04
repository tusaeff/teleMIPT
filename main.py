import telebot
import parser


#print(bot.get_me())

def log(message, answer):
    print("\n-------")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \nТекст: '{3}' \nОтвет: '{4}'".format(message.from_user.first_name,
                                                                                  message.from_user.last_name,
                                                                                  str(message.from_user.id),
                                                                                  message.text,
                                                                                  answer))



@bot.message_handler(content_types=['text'])
def handle_text(message):
        if message.text:
            result = parser.finalSearch(message.text)
            if (type(result) == list):
                for item in result:
                    bot.send_message(message.chat.id, item['name'] + ' - ' + item['href'])
            elif (type(result) == dict):
                for key in result:
                    if (type(result[key]) == list):
                        for item in result[key]:
                            bot.send_message(message.chat.id, item['skill'] + '  -  ' + item['value'])
                    elif (key == 'image'):
                            bot.send_message(message.chat.id, key + ' - http://wikimipt.org/' + result[key])
                    else:
                        if (key == 'name'):
                            bot.send_message(message.chat.id, result[key])
            else:
                bot.send_message(message.chat.id, 'Ничего не найдено')
           #log(message,answer)

# @bot.message_handler(content_types=['text'])
# def handle_text(message):
#    if message.text == "mipt":
#        answer = "idi botamy"
#        bot.send_message(message.chat.id, "idi botay")
#        log(message,answer)

# @bot.message_handler(commands=['start'])
# def keyboard(message):
#     user_markup = telebot.types.ReplyKeyboardMarkup(True)
#     user_markup.row('/start')
#     bot.send_message(message.from_user.id, 'здрасте', reply_markup=user_markup)

bot.polling(none_stop=True, interval=0)
