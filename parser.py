#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup;
import re
import requests;
import unicodedata
url_base = 'http://wikimipt.org/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B8_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from='
def getPrepList(name):
	url = url_base + name[0].upper()
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	rawPrepList = soup.find(class_ ="mw-category-group")
	if not rawPrepList:
		rawPrepList = soup.find(class_ ="mw-content-ltr")
	rawPrepList = rawPrepList.find('ul').children
	result = []
	for rawItem in rawPrepList:
		cleanItem = list(rawItem.children)[0]
		result.append({'name' : cleanItem['title'].lower(), 'href' : cleanItem['href']})
	return result
def findPrepInList(name, array):
	pattern = re.compile(name.lower())
	for item in array:
		if pattern.match(item['name']): 
			return 'http://wikimipt.org' + item['href']
def getPrepInfo(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	#print(url)
	items = list(soup.find(class_="wikitable card").children)
	resultObj = {}
	resultObj["name"] = items[1].get_text().strip()
	resultObj["image"] = items[3].find('td').find('img')['src']
	rating = list(soup.find(class_="wikitable card").find_all(class_='starrating-div'))
	resultObj['rate'] = []
	skills = [u'Знания', u'Умение преподавать', u'В общении', u'Халявность', u'Общая оценка']
	for key in range(0, 5):
		skillRate = rating[key].find('span').get_text()
		resultObj['rate'].append({'skill': skills[key], 'num' : key,  'rate' : skillRate})
	return resultObj

def finalSearch(name):
	result = findPrepInList(name, getPrepList(name))
	if(result):
		return getPrepInfo(result)


result = finalSearch(u'ипа')
print( u'Имя' + '  -  ' + result['name'])
for item in result['rate']:
	print(unicode(item['skill']) + u'  -  ' + item['rate'] )



#findPrepInList(u'Бурлуцкая', getPrepList(u'Бурлуцкая'))

# result = []
# for rawItem in prepList:
# 	item = BeautifulSoup(rawItem.unicode(), 'html.parser')
#print(rawPrepList)
		
