#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


# In[3]:


def get_all_links():
    """Получить все ссылки"""
    refs = []
    for i in range(50):
        page = str(i+1)
        URL = 'https://habr.com/ru/all/page' + page
        req = requests.get(URL)
        time.sleep(0.3)
        soup = BeautifulSoup(req.text, 'html.parser')
        new_block = soup.find_all('article', class_ = 'post')
        new_titles = list(map(lambda x: x.find('h2', class_ = 'post__title'), new_block))
        refs += list(map(lambda x: x.find('a').get('href'), new_titles))
    return refs


# In[4]:


res = get_all_links()


# In[8]:


def parsing():
    """
    Проверяет наличие слов keyword в каждой ссылке списка res и сохраняет дату, заголовок, ссылку и тест статьи в таблицу
    """
    keywords = ['парсинг']
    file = pd.DataFrame()
    for link in res:
        soup = BeautifulSoup(requests.get(link).text, 'html.parser')
        time.sleep(0.1)
        new_block = soup.find('div', class_ = 'post__text').text
        for word in keywords:
            if word in new_block:
                date = pd.to_datetime(soup.find('header', class_ = 'post__meta').find('span', class_ = 'post__time').get('data-time_published'), dayfirst = True).date()
                title = soup.find('h1', class_ = 'post__title post__title_full').find('span', class_ = 'post__title-text').text
                text = new_block.strip()
                row = {'date': date, 'title': title, 'link' : link, 'text': text}
                file = pd.concat([file, pd.DataFrame([row])])
    return file


# In[9]:


file = parsing()
file


# In[10]:


file.to_excel('file_parsing.xlsx', index = False)

