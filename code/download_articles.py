# -*- coding: utf-8 -*-
__author__ = 'sweeterr at gmail.com'


'''
This module downloads articles from http://sem.ruslang.ru/slovnik.php
and writes them into a folder 'articles/{letter}.

Input: login and password for the site.
Output: A folder with articles, prints out downloaded letters and
the number of vocables for each letter.
'''


# install requests for python http://docs.python-requests.org/en/master/
import requests
import re
import time
import os


# input login and password for http://sem.ruslang.ru/slovnik.php
AUTHENTICATION = 'login', 'password'


RE_LINE = re.compile('<td bgcolor=.+?<a href="(.+?)">(.+?)</a>.+?>(\[.*?\])<')
RE_ROW = re.compile('<tr onClick.+?</tr>', flags=re.DOTALL)
RE_LINK = re.compile('<a href="(.+?)">', flags=re.DOTALL)
RE_AUTHOR = re.compile('>(\[.*?\])<', flags=re.DOTALL)
RE_WORD1 = re.compile('<a href=".+?">(.+?)</a>', flags=re.DOTALL)
RE_WORD2 = re.compile('<nobr>(.+?)</nobr>', flags=re.DOTALL)


# makes a folder for the specified letter, goes through the lines of
# code for the letter, initiates search for vocables and saving vocable
# articles. Returns the downloaded number of vocables.
def download_articles(main_url, letter, articles_path):
    c = 0
    finished = False
    current_url = u'?letter={}'.format(letter)
    letter_articles_path = os.path.join(articles_path, letter)
    if not os.path.exists(letter_articles_path):
        os.mkdir(letter_articles_path)
    while not finished:
        text = requests.get(main_url + current_url, auth=AUTHENTICATION).text
        rows = RE_ROW.findall(text)
        for row in rows:
            word, link, author = get_data(row)
            c += 1
            check = check_first_letter(word[0], letter)
            if not check:
                finished = True
                break
            write_vocable(word, author, link, letter_articles_path)
        m = re.search('<a href="([^"]+?)">\[Вперед &gt;&gt;\]', text)
        if m and not finished:
            current_url = m.group(1)
        else:
            break
    print(letter, c-1)


# writes a vocable, author, vocable article link, and vocable article to file
# if there is no article yet, the article is written as 'not given'
def write_vocable(word, author, link, letter_articles_path):
    if link == 'not given':
        text = '{}\n{}\n{}\nnot given'.format(word, author, link)
    else:
        full_link = '{}{}'.format(main_url, link)
        article = download_vocable(full_link)
        text = '{}\n{}\n{}\n{}'.format(word, author, full_link, article)
    vocable_path = os.path.join(letter_articles_path, '{}.txt'.format(word))
    write_to_file(text, vocable_path)


# checks if the first letter of the vocable is identical to the working letter
def check_first_letter(first_letter, letter):
    check = True
    if letter == 'е':
        if first_letter in 'еЕёЁ':
            pass
        else:
            check = False
    else:
        if first_letter == letter or first_letter == letter.upper():
            pass
        else:
            check = False
    return check


# extracts a vocable, link to vocable article, and author from a line of code
def get_data(row):
    w = RE_WORD1.search(row)  # if the vocable article exists and there is a link
    if w:
        word = w.group(1)
    else:                       # if the article is not written and there is no link
        word = RE_WORD2.search(row).group(1)
    link = 'not given'  # if the article for the word is not written yet
    l = RE_LINK.search(row)
    if l:
        link = l.group(1)
    author = 'not given' # no idea if that happens, however '[]' are present
    a = RE_AUTHOR.search(row)
    if a:
        author = a.group(1)
    return word, link, author


# downloads code from the vocable page
def download_vocable(link):
    page = requests.get(link, auth=('s', 's'))
    text = re.sub(u'.+<hr>', u'', page.text, flags=re.DOTALL)  # remove header
    return text


# writes a text to file with supplied path
def write_to_file(text, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


# goes through a list of letters and initiates search for vocables for
# each letter
if __name__ == u'__main__':
    start_time = time.time()
    main_url = u'http://sem.ruslang.ru/slovnik.php'
    letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    articles_path = 'articles'
    if not os.path.exists(articles_path):
        os.mkdir(articles_path)
    for letter in letters:
        download_articles(main_url, letter, articles_path)
    print('{} seconds'.format(time.time() - start_time))