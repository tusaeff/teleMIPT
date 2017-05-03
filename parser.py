#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup;
import re
import requests;
import unicodedata
url_base = 'http://wikimipt.org/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B8_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from='
def getPrepList(name):# здесь получаем список препов с викимипта(тех чьи фамилии на нужную букву начинаются)
	url = url_base + name[0].upper()#получаем нужную ссылку(посмотри на викимипте как она выглядит)
	r = requests.get(url)#получаем страницу
	if( r.status_code == 200):
		soup = BeautifulSoup(r.text, 'html.parser')#запускаем парсер
		rawPrepList = soup.find(class_ ="mw-category-group")#находим нужный блок
		if not rawPrepList:
			rawPrepList = soup.find(class_ ="mw-content-ltr")#викимипт стремный, там короче страница на Я по другому устроенаб поэтому так
		rawPrepList = rawPrepList.find('ul').find_all('li')#дальше пробираемс по тегам к нужным данным
		result = []
		for rawItem in rawPrepList:
			cleanItem = list(rawItem.children)[0]
			result.append({'name' : cleanItem['title'].lower(), 'href' : cleanItem['href']})#получаем массив всех препов с именем и ссылкой
		return result
	else:
		raise ValueError('Невозможно получить список преподавателей ((00((00(((' + ' - ' + r.status_code)# код 200 это типа хороший ответ, а на все остальное мы генерим ошибки
def findPrepInList(name, array):# здесь находим нужного препа в списке()
	result = []
	pattern = re.compile(name.lower())# получаем нужное регулярное выражение(загугли если не шаришь); регулярка а не поиск по подстроке потому что возможно поиск над будет улучшить - такой задел на будущее
	for item in array:
		if pattern.match(item['name']): # ну и просто сверяем все имена с регуляркой
			result.append({'name' : item['name'], 'href' : 'http://wikimipt.org' + item['href']})
	return result;
def getPrepInfo(url):#получаем инфу по конкретному препу(тут короче все так же, поэтому не буду особо расписывать)
	r = requests.get(url)
	if( r.status_code == 200):
		soup = BeautifulSoup(r.text, 'html.parser')
		#print(url)
		items = list(soup.find(class_="wikitable card").children)
		resultObj = {}
		resultObj["name"] = items[1].get_text().strip()#strip типа удаляет лишние пробелы, а гет_техт получает текст тега
		resultObj["image"] = items[3].find('td').find('img')['src']
		rating = list(soup.find(class_="wikitable card").find_all(class_='starrating-div'))
		resultObj['rate'] = []
		skills = [u'Знания', u'Умение преподавать', u'В общении', u'Халявность', u'Общая оценка']
		for key in range(0, 5):
			skillRate = rating[key].find('span').get_text()
			resultObj['rate'].append({'skill': skills[key], 'num' : key,  'value' : skillRate})
		return resultObj
	else:
		raise ValueError('Невозможно получить страницу преподавателя (00((((((' + ' - ' + r.status_code)
def finalSearch(name):
	result = findPrepInList(name, getPrepList(name))
	if(len(result) != 0):
		if(len(result) == 1):
			return getPrepInfo(result[0]['href'])
		else:
			return result;


def formatOutput(result):
	if (type(result) == list):
		for item in result:
			print (item['name'] + ' - ' + item['href'])
	elif (type(result) == dict):
		for key in result:
			if (type(result[key]) == list):
				for item in result[key]:
					print (item['skill'] + '  -  ' + item['value'])
			else:
				print key + ' - ' + result[key]
	else:
		print(u'Ничего не найдено')
formatOutput(finalSearch(u'беклемишев'))


# def emojify(num):
# 	if(num >= 4.5):
# 		return '❤️❤️❤️❤️❤️'
# 	if num/1 = 4 :
# 		return '⭐️⭐️⭐️⭐️'
# 	elif num/1 = 3 : 
# 		return '⭐️⭐️⭐️'
# 	elif num/1 = 2 :
# 		return '🍆🍆'
# 	return '🆘'


#что тебе над знать - файнал серч может вернуть три типа значений - ноне(если такого препа нет, или проихошла ошибка(в консоли тогда смотри)) -
# в таком случае ты типа гришь извините препа нет или ошибка;
#еще может вернуть обьект - тогда все четко; у обьекта(или словаря, это вроде  так здесь называется) 
# есть три поля - name, image и rate, rate - это массив, который состоит из обьктов у которых в поле skill записано типа 'Халявность' там и всякое в таком духе
# а в поле value - значение(это строка, правда - там еще количество голосов есть)
#ну и последнее - файнал серч может вернуть массив - тогда это означает что у нас типа несколько совпадений (массив - тоже обьектов, там поля типа name и href где чего вроде понятно из названия)
#

