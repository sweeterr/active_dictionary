# -*- coding: utf-8 -*-
__author__ = 'sweeterr at gmail.com'


import re
import html
import time
import os


# cleans up a text file with given path
def clean_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        new_text = '{}{}{}'.format(lines[0], lines[1], lines[2])
        for line in lines[3:]:
            line = re.sub('\n|\r', ' ', line)                       # sub breaks with spaces
            line = re.sub('<p', '\n<p', line)                       # make paragraphs
            line = re.sub('<.+?>', '', line)                        # remove all tags
            line = html.unescape(line)                              # decode html symbols
            line = re.sub('\n +', '\n', line)                       # del starting space
            line = re.sub('^ +', '', line)                          # del other starting space
            line = re.sub(u' ', u' ', line)                         # sub nbrspace with regular space
            line = re.sub('([AА][0-9]+) % ', '\g<1>\t•\t', line)    # arg model with tabs
            line = re.sub('% ', '\t•\t', line)                      # arg model with tabs
            line = re.sub(' +', u' ', line)                         # delete multiple spaces
            line = re.sub(' ([.,!;:)])', '\g<1>', line)             # del spaces before punctuation
            new_text = '{}{}'.format(new_text, line)
        new_text = re.sub('\n +', '\n', new_text, flags=re.MULTILINE)               # del starting spaces
        new_text = re.sub('\s+\n', '\n', new_text, flags=re.MULTILINE)              # del ending white space
        new_text = re.sub('\n+', '\n', new_text, flags=re.MULTILINE)                # del mult breaks
        new_text = re.sub('\n\t([^•])', '\n\g<1>', new_text, flags=re.MULTILINE)    # del rogue tabs
    return new_text


# reads a file with a given path, returns file text
def read_file(path):
    with open(path, u'r', encoding='utf-8') as f:
        return f.read()


# writes a text to a given path
def write_to_file(text, path):
    with open(path, u'w', encoding='utf-8') as f:
        f.write(text)


# reads articles from a given path1, writes clean articles to
# a given path2
def clean_articles(path1, path2):
    if not os.path.exists(path2):
        os.mkdir(path2)
    for root, dirs, files in os.walk(path1):
        for d in dirs:
            dir_path = os.path.join(path2, d)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                text = clean_text(file_path)
                new_file_path = file_path.replace(path1, path2)
                write_to_file(text, new_file_path)


# combines vocable files into one file according to starting letter
def get_letter_volumes(path1, path2):
    if not os.path.exists(path2):
        os.mkdir(path2)
    for root, dirs, files in os.walk(path1):
        for d in dirs:
            text = ''
            dir_path = os.path.join(path1, d)
            for d_root, d_dirs, d_files in os.walk(dir_path):
                for file_name in d_files:
                    file_path = os.path.join(d_root, file_name)
                    text = '{}\n{}'.format(text, read_file(file_path))
            volume_path = os.path.join(path2, '{}.txt'.format(d))
            write_to_file(text, volume_path)


# initiates a clean up of articles in folder with articles_path
# and saving clean articles to folder with clean_articles_path.
# initiates getting a volume for each letter
if __name__ == u'__main__':
    start_time = time.time()
    articles_path = 'articles'
    clean_articles_path = 'clean_articles'
    clean_articles(articles_path, clean_articles_path)
    get_letter_volumes(clean_articles_path, 'letter_volumes')
    print('{} seconds'.format(time.time() - start_time))