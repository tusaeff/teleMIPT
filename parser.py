#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup;
import re
import requests;
import unicodedata
import time
url_base = 'http://wikimipt.org/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B8_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from='
IS_TESTING = True
def test(func):
	if(not IS_TESTING):
		def run_test(*args):
			return func(*args)
	else:
		def run_test(*args):
			t0 = time.time()
			x = func(*args)
			t1 = time.time()
			print (func.__name__ + ' - ' + str(t1 - t0))
			return x
	return run_test
@test
def getPrepList(name):# здесь получаем список препов с викимипта(тех чьи фамилии на нужную букву начинаются)
	url = url_base + name[0].upper()#получаем нужную ссылку(посмотри на викимипте как она выглядит)
	r = requests.get(url)#получаем страницу
	if( r.status_code == 200 ):
		soup = BeautifulSoup(r.text, 'html.parser')#запускаем парсер
		rawPrepList = soup.find(class_ ="mw-category-group")#находим нужный блок
		if not rawPrepList:
			rawPrepList = soup.find(class_ ="mw-content-ltr")#викимипт стремный, там короче страница на Я по другому устроена поэтому так
		rawPrepList = rawPrepList.find('ul').find_all('li')#дальше пробираемся по тегам к нужным данным
		result = []
		for rawItem in rawPrepList:
			cleanItem = list(rawItem.children)[0]
			result.append({'name' : cleanItem['title'], 'href' : cleanItem['href']})#получаем массив всех препов с именем и ссылкой
		return result
	else:
		raise ValueError('Невозможно получить список преподавателей ((00((00(((' + ' - ' + r.status_code)# код 200 это типа хороший ответ, а на все остальное мы генерим ошибки
@test	
def findPrepInList(name, array):# здесь находим нужного препа в списке
	result = []
	pattern = re.compile(name.lower(), flags=re.IGNORECASE)# получаем нужное регулярное выражение 
	for item in array:
		if pattern.match(item['name']): # ну и просто сверяем все имена с регуляркой
			result.append({'name' : item['name'], 'href' : 'http://wikimipt.org' + item['href']})
	return result;
@test
def getPrepInfo(url):#получаем инфу по конкретному препу(тут короче все так же)
	r = requests.get(url)
	if( r.status_code == 200):
		soup = BeautifulSoup(r.text, 'html.parser')
		#print(url)
		items = list(soup.find(class_="wikitable card").children)
		resultObj = {}
		resultObj["name"] = items[1].find('b').get_text().strip()#strip типа удаляет лишние пробелы, а гет_техт получает текст тега
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
@test
def finalSearch(name):
	result = findPrepInList(name, getPrepList(name))
	if(len(result) != 0):
		if(len(result) == 1):
			return getPrepInfo(result[0]['href'])
		else:
			return result;


#файнал серч может вернуть три варианта:
#1)ноне(если такого препа нет, или проихошла ошибка)
#2)вернуть обьект, у которого есть три поля - name, image и rate, rate - это массив, который состоит 
#из обьктов у которых в поле skill записано типа 'Халявность' и прочее,
#а в поле value - значение(это строка - там еще количество голосов есть)
#3)массив - тогда это означает что у нас типа несколько совпадений (массив - тоже обьектов)

