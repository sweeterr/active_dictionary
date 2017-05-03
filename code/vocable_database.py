# -*- coding: utf-8 -*-
__author__ = 'sweeterr at gmail.com'


'''
This module creates a list of vocables (class Vocable) for specified
letters from a directory of clean vocable files, which could be further
written to a .csv or .db file.
'''


import re
import time
import os
import csv
import sqlite3


class Vocable:
    def __init__(self, vocable=None, article=None, synopsis=None,
                 pos=None, lexemes=None, articles=None,
                 definitions=None, arguments=None, models=None,
                 author=None, link=None):
        self.vocable = vocable
        self.article = article
        self.synopsis = synopsis
        self.pos = pos
        self.lexemes = lexemes
        self.articles = articles
        self.definitions = definitions
        self.arguments = arguments
        self.models = models
        self.author = author
        self.link = link


# reads a file with a given path, returns file text
def read_file(path):
    with open(path, u'r', encoding='utf-8') as f:
        return f.read()


# writes a text to a given path
def write_to_file(text, path):
    with open(path, u'w', encoding='utf-8') as f:
        f.write(text)


# extracts part of speech from vocable article. A mistake is possible
# if POS are annotated in a non-standard way.
def get_pos(text):
    part_of_speech = 'not given'
    pos = re.search(', ([А-ЯЁ]+)', text)
    if pos:
        part_of_speech = pos.group(1)
    return part_of_speech


# extracts a list of lexemes and lexeme articles from a vocable article
# A mistake is possible if the lexemes are enumerated incorrectly.
def get_lexemes(vocable, text):
    lexemes, articles = [], []
    vocable = re.sub('[0-9 ]+$', '', vocable)

    # lets find all vocables with numbers at the start of the lines
    # -- potential lexemes
    first = vocable[0].upper() + vocable[0].lower()
    if vocable[0] in 'еЕёЁ':
        first = 'еЕёЁ'
    l = re.findall('\n([' + first + ']' + vocable[1:]
                   + ' [0-9]+([-–][0-9]+)?(\.)?([0-9]+([-–][0-9]+)?)?)', text)

    # if there are no vocables with numbers, there are no separate lexemes
    if len(l) == 0:
        lexemes.append(vocable)
        articles.append(text)

    # if there are separate lexemes
    else:

        # make a lexeme list
        for lexeme in l:
            if lexeme[0] not in lexemes:
                lexemes.append(lexeme[0])

        # search for lexeme articles
        for i in range(len(lexemes) - 1):

            # a strinf from starting lexeme to next starting lexeme
            matches = re.findall('\n(' + lexemes[i] + '.+?)\n' +
            #matches = re.findall('\n(' + lexemes[i] + '.+?)' +
                                 lexemes[i+1], text, flags=re.S)

            # if one match -- i. e. no synopsis
            if len(matches) == 1:
                articles.append(matches[0])

            # if there is synopsis, we take second match, i. e. article
            if len(matches) == 2:
                articles.append(matches[1])

        # final lexeme has no next lexeme
        final = re.search('(\n' + lexemes[-1] + '(.+?))$', text, flags=re.S)
        matches = re.findall('\n' + lexemes[-1], final.group(1))
        if len(matches) > 1:
            match = re.search('\n(' + lexemes[-1] + '.+?)$',
                              final.group(2), flags=re.S)
            if match:
                articles.append(match.group(1))
            else:
                articles.append('not given')
                print(vocable, ': problem with lexeme articles')
        elif len(matches) == 1:
            articles.append(final.group(1))
        else:
            articles.append('not given')
            print(vocable, ': problem with lexeme articles')
    return lexemes, articles


# extracts a synopsis from a vocable article
def get_synopsis(lexemes, text):
    synopsis = 'not given'
    if len(lexemes) > 1:
        match = re.search('\n(' + lexemes[0] + '.+?)\n' + lexemes[0] + '[^.]', text, flags=re.S)
        if match:
            synopsis = match.group(1)
    return synopsis


# extracts a definition from a lexeme article
def get_definition(text):
    definition = 'not given'
    def_lex = re.search('ЗНАЧЕНИЕ(\.|:)?.(.+?)(\n|$)', text)
    if def_lex:
        definition = def_lex.group(2)
    return definition


# extracts arguments from a definition
def get_arguments(text):
    args = re.findall('[AА][0-9]+', text)
    if len(args) > 0:
        arguments = []
        for arg in args:
            if arg not in arguments:
                arguments.append(arg)
        return ';'.join(sorted(arguments))
    else:
        return 'not given'


# extracts a government model from a lexeme article
def get_model(text, args):
    model = ''
    if args[0] == 'not given':
        model = 'not given'
    else:
        lines = re.findall('\n((([AА][0-9]+\t+•\t)|(\t•\t)).+)', text)
        for line in lines:
            model += re.sub('\n', '\t', line[0])
        if len(lines) == 0:
            model = u'not given'
    return model


# walks through vocable files and initiates part of speech, lexeme, lexeme
# article, synopsis, lexeme definitions, lexeme arguments, lexeme models
# extraction. Returns a list of vocables with all attributes.
def get_vocables(path):
    vocables = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                vocable, author, link = lines[0].strip(), \
                                        lines[1].strip(), \
                                        lines[2].strip()
                article = ''.join(lines[3:])
                pos = get_pos(article)
                lexemes, articles = get_lexemes(vocable, article)
                synopsis = get_synopsis(lexemes, article)
                definitions, arguments, models = [], [], []
                for i in range(len(lexemes)):
                    try:
                        definitions.append(get_definition(articles[i]))
                        arguments.append(get_arguments(definitions[i]))
                        models.append(get_model(articles[i], arguments[i]))

                    # if there is a mistake with parsing or numbering of lexemes and lexeme articles,
                    # the number of lexemes might not be equal to the number of lexeme articles
                    # (2017/05/02: же)
                    except IndexError:
                        print('index error -- {}'.format(vocable))
                vocables.append(Vocable(vocable, article, synopsis,
                                        pos, lexemes, articles,
                                        definitions, arguments,
                                        models, author, link))
    return vocables


# given a list of vocables with all attributes, writes them to a .csv file
# with specified path.
def write_vocables_to_file(vocables, path):
    with open(path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='#')
        for v in vocables:
            for i in range(len(v.lexemes)):
                try:
                    writer.writerow((v.vocable, v.author, v.pos, v.lexemes[i],
                                     v.definitions[i], v.arguments[i], v.models[i]))

                # same as in get_vocables – there might be problems with numbering or parsing
                # of lexemes and lexeme articles (2017/05/02: завалить)
                except IndexError:
                    print('index error -- {}'.format(v.vocable))


# writes vocables with synopses to a specified file
def print_synopsis(vocables, path):
    with open(path, 'w', encoding='utf-8') as f:
        for v in vocables:
            if v.synopsis != 'not given':
                f.write('{}\n{}\n\n'.format(v.vocable, v.synopsis))


# creates a vocable database with two tables: vocables and lexemes
def create_vocable_db(path):
    if os.path.exists(path):
        os.remove(path)
    c = sqlite3.connect(path)
    cursor = c.cursor()
    cursor.execute('CREATE TABLE vocables (vocable TEXT PRIMARY KEY, synopsis TEXT, author TEXT, '
                   'pos TEXT, link TEXT, article TEXT)')
    cursor.execute('CREATE TABLE lexemes (vocable TEXT, lexeme TEXT, definition TEXT,'
                   ' arguments TEXT, models TEXT, lexeme_article TEXT, PRIMARY KEY (vocable, lexeme))')
    c.commit()


# writes vocables to a specified vocable database file
def fill_vocable_db(vocables, path):
    c = sqlite3.connect(path)
    cursor = c.cursor()
    for v in vocables:
        try:
            cursor.execute('INSERT INTO vocables VALUES (?, ?, ?, ?, ?, ?)',
                           (v.vocable, v.synopsis, v.author, v.pos, v.link, v.article))

        # if there are absolute vocable duplicates, only one is written
        except sqlite3.IntegrityError:
            print('sql vocable -- {}'.format(v.vocable))
        for i in range(len(v.lexemes)):
            try:
                cursor.execute('INSERT INTO lexemes VALUES (?, ?, ?, ?, ?, ?)',
                               (v.vocable, v.lexemes[i], v.definitions[i],
                                v.arguments[i], v.models[i], v.articles[i]))

            # same as in get_vocables – there might be problems with numbering or parsing
            # of lexemes and lexeme articles
            # (2017/05/02: затянуть + несколько пустых)
            except IndexError:
                print('index -- {}'.format(v.vocable))

            # if there are absolute lexeme duplicates, only one is written
            # (2017/05/02: затянуть + несколько пустых)
            except sqlite3.IntegrityError:
                print('sql lexeme -- {}'.format(v.vocable))
    c.commit()


# combines letter databases into volumes (of 4 as of 2017/05/02)
def db_into_volumes(main, others):
    create_vocable_db('../databases/{}.db'.format(main))
    c = sqlite3.connect('../databases/{}.db'.format(main))
    cursor = c.cursor()
    for other in others:
        cursor.execute('ATTACH "../databases/{}.db" AS {}'.format(other, other))
        cursor.execute('INSERT INTO vocables SELECT * FROM {}.vocables'.format(other))
        cursor.execute('INSERT INTO lexemes SELECT * FROM {}.lexemes'.format(other))
    c.commit()


# initiates vocable collection from files, recording vocables to
# a .csv and .db files for each letter
if __name__ == '__main__':
    start_time = time.time()
    letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    if not os.path.exists('../letter_tables_csv'):
        os.mkdir('../letter_tables_csv')
    if not os.path.exists('../synopses'):
        os.mkdir('../synopses')
    if not os.path.exists('../databases'):
        os.mkdir('../databases')
    for letter in letters:
        vocables = get_vocables('../clean_articles/{}'.format(letter))
        write_vocables_to_file(vocables, '../letter_tables_csv/whole_table_{}.csv'.format(letter))
        #print_synopsis(vocables, '../synopses/synopsis_{}.txt'.format(letter))
        create_vocable_db('../databases/db_{}.db'.format(letter))
        fill_vocable_db(vocables, '../databases/db_{}.db'.format(letter))

    # combine letter databases into one volume
    to_combine_1 = ['db_а', 'db_б', 'db_в', 'db_г']
    to_combine_2 = ['db_д', 'db_е', 'db_ж', 'db_з']
    db_into_volumes('db_volume_1', to_combine_1)
    db_into_volumes('db_volume_2', to_combine_2)

    print('{} seconds'.format(time.time() - start_time))