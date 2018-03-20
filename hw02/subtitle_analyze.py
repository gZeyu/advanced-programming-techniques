# -*- coding: utf-8 -*-
import sys
import re
import timeit


def format_time(time_string):

    elements = re.split(r'[:,]', time_string)
    hours = int(elements[0])
    minutes = int(elements[1])
    seconds = int(elements[2])
    milliseconds = int(elements[3])
    time_stamp = ((hours * 60 + minutes) * 60 + seconds) * 1000 + milliseconds

    return time_stamp


def segment_word(text):

    pattern = r'''
        (?x)                   # set flag to allow verbose regexps
        (?:[A-Z]\.)+           # abbreviations, e.g. U.S.A.
        |\d+(?:\.\d+)?%?       # numbers, incl. currency and percentages
        |\w+(?:[-']\w+)*       # words w/ optional internal hyphens/apostrophe
        # |(?:[+/\-@&*])         # special characters with meanings
        # |\S\w*                 # any sequence of word characters#
        # |[][{}.,;"'?():_`-]    # these are separate tokens
        '''
    word_list = re.findall(pattern, text)
    return word_list


def read_subtitle_file(filename):

    milliseconds = 0
    word_count = 0

    with open(filename, 'r') as file:
        text = file.readlines()
        for i in range(len(text)):
            if '-->' in text[i]:
                elements = text[i].split()
                milliseconds += format_time(elements[2]) - format_time(
                    elements[0])
                word_count += len(segment_word(text[i + 1]))
    frequency = word_count / (milliseconds / 60000)

    # print(word_count)
    # print(milliseconds / 60000)
    return frequency


def func():
    read_subtitle_file('discoverycuriositys01e06.eng.srt')


if __name__ == '__main__':

    t = timeit.repeat(
        'func()', 'from __main__ import func', number=1, repeat=5)
    print(t)
    print(min(t))
