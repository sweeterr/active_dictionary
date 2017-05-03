# -*- coding: utf-8 -*-
__author__ = 'sweeterr at gmail.com'


'''
This module checks if all arguments in the definition of the lexeme
have a government model. Lexemes with arguments without models are
written to specified file.
'''


import re
import time
import os


# given a path to vocable files, checks if all arguments in the
# definition of the lexeme have a government model. Writes lexemes
# with arguments without models to specified file.
def check_models(path1, path2):
    without_model = ''
    for root, dirs, files in os.walk(path1):
        for file_name in files:
            if file_name.endswith('.csv'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        elements = line.split('#')
                        if elements[5] != 'not given':
                            args = elements[5].split(';')
                            args = [arg.strip('AА') for arg in args]
                            for arg in args:
                                match = re.search('[AА]' + arg + '\t+•\t', elements[6])
                                if not match:
                                    without_model += '{}#{}#{}#{}#{}#A{}#{}'.format(elements[0], elements[1],
                                                                                    elements[2], elements[3],
                                                                                    elements[4], arg, elements[6])
    with open(path2, 'w', encoding='utf-8') as f:
        f.write(without_model)


# initiates the check
if __name__ == '__main__':
    start_time = time.time()
    tables_path = '../letter_tables_csv'
    if not os.path.exists('../check_results'):
        os.mkdir('../check_results')
    check_models(tables_path, '../check_results/without_model.csv')
    print('{} seconds'.format(time.time() - start_time))