# -*- coding: utf-8 -*-
__author__ = 'sweeterr at gmail.com'


'''
This module checks if lexeme enumeration in synopses and articles is
consistent. Vocables with inconsistencies are written to specified file.
'''


import re
import time
import os


# creates a dictionary with vocables as keys and lexeme numbers as values
def get_num_dict(path):
    voc_dict = dict()
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.csv'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        elements = line.split('#')
                        nums = re.search('[0-9-–]+(\.)?[0-9-–]*', elements[3])
                        if nums:
                            if nums.group() not in '-–':
                                if elements[0] in voc_dict:
                                    voc_dict[elements[0]].append(nums.group())
                                else:
                                    voc_dict[elements[0]] = [nums.group()]
    return voc_dict


# prints out vocables which have lexeme numbers with dashes to a separate file
# converts string numbers to integers
def get_with_dashes(voc_dict, path):
    with_dashes = dict()
    for v in sorted(voc_dict):
        voc_dict[v] = [num.split('.') for num in voc_dict[v]]
        int_nums = []
        for nums in voc_dict[v]:
            try:
                nums = [int(num) for num in nums if num != '']
                int_nums.append(nums)
            except ValueError:
                with_dashes[v] = voc_dict[v]
        voc_dict[v] = int_nums
    with open(path, 'w', encoding='utf-8') as f:
        for v in with_dashes:
            line = '{} {}\n'.format(v, with_dashes[v])
            f.write(line)
    return voc_dict


# checks if lexeme numbers are consistent
# prints out vocables with suspicious lexeme numbers to specified file
def check_enumeration(voc_dict, path):
    wonky_vocables = dict()
    for v in voc_dict:

        # go through all lexemes apart from last
        for i in range(len(voc_dict[v])-1):

            # if there is no dot for current lexeme
            if len(voc_dict[v][i]) == 1:

                # check first lexeme
                if i == 0:
                    if voc_dict[v][i][0] != 1:
                        wonky_vocables[v] = voc_dict[v]

                # if there is no dot for next lexeme
                if len(voc_dict[v][i+1]) == 1:
                    if not (voc_dict[v][i][0]+1 == voc_dict[v][i+1][0]):
                        wonky_vocables[v] = voc_dict[v]

                # if there is a dot for next lexeme
                else:
                    if not ((voc_dict[v][i+1][0] == voc_dict[v][i][0]+1)
                            and (voc_dict[v][i+1][1] == 1)):
                        wonky_vocables[v] = voc_dict[v]

            # if there is a dot in current lexeme
            else:

                # check first lexeme
                if i == 0:
                    if (voc_dict[v][i][0] != 1) and (voc_dict[v][i][1] != 1):
                        wonky_vocables[v] = voc_dict[v]

                # if there is no dot for next lexeme
                if len(voc_dict[v][i+1]) == 1:
                    if not (voc_dict[v][i][0]+1 == voc_dict[v][i+1][0]):
                        wonky_vocables[v] = voc_dict[v]

                # if there is a dot for next lexeme
                else:
                    if not ((voc_dict[v][i+1][0] == voc_dict[v][i][0]
                             and voc_dict[v][i+1][1] == voc_dict[v][i][1]+1)
                            or (voc_dict[v][i+1][0] == voc_dict[v][i][0]+1
                                and voc_dict[v][i+1][1] == 1)):
                        wonky_vocables[v] = voc_dict[v]
    with open(path, 'w', encoding='utf-8') as f:
        for v in sorted(wonky_vocables):
            line = '{} {}\n'.format(v, wonky_vocables[v])
            f.write(line)


# initiates the check
if __name__ == '__main__':
    start_time = time.time()
    tables_path = '../letter_tables_csv'
    if not os.path.exists('../check_results'):
        os.mkdir('../check_results')
    num_dict = get_num_dict(tables_path)
    num_dict = get_with_dashes(num_dict, '../check_results/with_dashes.txt')
    check_enumeration(num_dict, '../check_results/wonky_numbers.txt')
    print('{} seconds'.format(time.time() - start_time))