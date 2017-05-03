# -*- coding: utf-8 -*-
__author__ = 'sweeterr at gmail.com'


'''
This module checks if A1 argument is present in the definition
of the lexeme, where there are at all arguments. Lexemes without
relevant A1 argument are written to specified file.
'''


import re
import time
import os


# given a path to vocable files, checks if A1 argument is present,
# where there are at all arguments. Writes lexemes without A1 argument
# to specified file.
def check_a1(path1, path2):
    without_a1 = ''
    for root, dirs, files in os.walk(path1):
        for file_name in files:
            if file_name.endswith('.csv'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        elements = line.split('#')
                        if elements[5] != 'not given':
                            match = re.search('[AА]1', elements[5])
                            if not match:
                                without_a1 += '{}#{}#{}#{}#{}\n'.format(elements[0], elements[1],
                                                                        elements[2], elements[3],
                                                                        elements[4])
    with open(path2, 'w', encoding='utf-8') as f:
        f.write(without_a1)


# initiates the check
if __name__ == '__main__':
    start_time = time.time()
    tables_path = '../letter_tables_csv'
    if not os.path.exists('../check_results'):
        os.mkdir('../check_results')
    check_a1(tables_path, '../check_results/without_a1.csv')
    print('{} seconds'.format(time.time() - start_time))