#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import requests
import unicodedata
import time
url_base = 'http://wikimipt.org/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B8_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from='
IS_TESTING = False
print ('\n -----------')


def test(func):
    """декоратор для анализа времени выполнения разных функций парсера"""
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


def getPrepList(name):
    """получает список препов с викимипта(тех чьи фамилии на нужную букву начинаются)"""
    url = url_base + name[0].upper()
    r = requests.get(url)
    if(r.status_code == 200):
        soup = BeautifulSoup(r.text, 'html.parser')
        rawPrepList = soup.find(
            class_="mw-category-group")
        if not rawPrepList:
            rawPrepList = soup.find(class_="mw-content-ltr")
        rawPrepList = rawPrepList.find('ul').find_all('li')
        result = []
        for rawItem in rawPrepList:
            cleanItem = list(rawItem.children)[0]
            result.append(
                {'name': cleanItem['title'], 'href': cleanItem['href']})
        return result
    else:
        raise ValueError(
            'Невозможно получить список преподавателей ((00((00(((' +
            ' - ' +
            r.status_code)


def findPrepInList(name, array):
    """находит нужного преподавателя в списке"""
    result = []
    pattern = re.compile(name.lower(), flags=re.IGNORECASE)
    for item in array:
        if pattern.match(
                item['name']):
            result.append(
                {'name': item['name'], 'href': 'http://wikimipt.org' + item['href']})
    return result


def getPrepInfo(url):
    '''получаем инфу по конкретному преподавателю'''
    r = requests.get(url)
    if(r.status_code == 200):
        soup = BeautifulSoup(r.text, 'html.parser')
        items = list(soup.find(class_="wikitable card").children)
        resultObj = {}
        resultObj["name"] = items[1].find('b').get_text().strip()
        resultObj["image"] = items[3].find('td').find('img')['src']
        resultObj["href"] = url
        rating = list(
            soup.find(
                class_="wikitable card").find_all(
                class_='starrating-div'))
        resultObj['rate'] = []
        resultObj['href'] = url
        skills = [
            u'Знания',
            u'Умение преподавать',
            u'В общении',
            u'Халявность',
            u'Общая оценка']
        for key in range(0, 5):
            skillRate = rating[key].find('span').get_text()
            resultObj['rate'].append(
                {'skill': skills[key], 'num': key, 'value': skillRate})
        return resultObj
    else:
        raise ValueError(
            'Невозможно получить страницу преподавателя (00((((((' + ' - ' + r.status_code)


def finalSearch(name):
    """получает список преподавателей с wikimipt.org и находит нужного"""
    result = findPrepInList(name, getPrepList(name))
    if(len(result) != 0):
        if(len(result) == 1):
            return getPrepInfo(result[0]['href'])
        else:
            return result
