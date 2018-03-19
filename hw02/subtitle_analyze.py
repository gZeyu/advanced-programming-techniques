# -*- coding: utf-8 -*-
import sys
import re


def time_format(time_string):

    elements = re.split(r'[:,]', time_string)
    hours = int(elements[0])
    minutes = int(elements[1])
    seconds = int(elements[2])
    milliseconds = int(elements[3])
    time_stamp = ((hours * 60 + minutes) * 60 + seconds) * 1000 + milliseconds

    return time_stamp


def read_subtitle_file(filename):

    milliseconds = 0
    with open(filename, 'r') as file:
        text = file.readlines()
        for i in range(len(text)):
            if '-->' in text[i]:
                elements = text[i].split()
                milliseconds += time_format(elements[2]) - time_format(
                    elements[0])
                print(text[i])
        # for line in text:
        #     if '-->' in line:
        #         elements = line.split()
        #         milliseconds += time_format(elements[2]) - time_format(
        #             elements[0])
        #         print(line)


if __name__ == '__main__':

    read_subtitle_file('discoverycuriositys01e06.eng.srt')
    # print(time_format('00:01:59,930'))
