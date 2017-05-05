# -*- coding: utf-8 -*-
__author__ = 'sweeterr at gmail.com'


'''
This module checks if lexeme starts with capital letter (which it
should not, apart from cases like Земля (планета)). If there is a
lexeme starting with capital letter, its vocable is written to a
specified file.
'''


import re
import time
import os


# prints vocables to specified file
def print_voc(vocables, path):
    with open(path, 'w', encoding='utf-8') as f:
        for v in sorted(vocables):
            line = '{}\n'.format(v)
            f.write(line)


# checks if there are lexemes starting with capital letter in
# a folder of vocable files.
def check_capital(path1, path2):
    vocables = set()
    for root, dirs, files in os.walk(path1):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                vocable = re.search('(.+)\.txt', file_name).group(1)
                cap_voc = '{}{}'.format(vocable[0].upper(), vocable[1:])
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    lex_cap = re.findall('\n\s*' + cap_voc + ' [0-9]+([-–][0-9]+)?(\.)?([0-9]+([-–][0-9]+)?)?', text)
                    if len(lex_cap) > 0:
                        vocables.add(vocable)
    print_voc(vocables, path2)


# initiates the check
if __name__ == '__main__':
    start_time = time.time()
    articles_path = '../clean_articles'
    if not os.path.exists('../check_results'):
        os.mkdir('../check_results')
    check_capital(articles_path, '../check_results/with_capitals.txt')
    print('{} seconds'.format(time.time() - start_time))