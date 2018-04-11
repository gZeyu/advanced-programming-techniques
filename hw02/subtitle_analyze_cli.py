# -*- coding: utf-8 -*-
import sys
import os
import re
import concurrent.futures
import threading
import timeit
import time
import math
import random
import queue
import chardet


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

def judge_pure_english(keyword):  
    return all(ord(c) < 128 for c in keyword)  


def read_subtitle_file(filename):
    # print(filename)
    milliseconds = 0
    word_count = 0
    file = open(filename, "rb")
    detector = chardet.UniversalDetector()
    for line in file.readlines()[0:10]:    
        detector.feed(line)    
        if detector.done:            
            break
    detector.close()
    file.close()
    # print(detector.result)
    with open(
            filename, 'r', encoding=detector.result['encoding'],
            errors='ignore') as file:
        text = file.readlines()
        for i in range(len(text)):
            if '-->' in text[i]:
                text[i] = text[i].replace('-->', ' --> ')
                elements = text[i].split()
                milliseconds += format_time(elements[2]) - format_time(
                    elements[0])
                for j in range(1,2):
                    if text[i + j].strip() == '':
                        break
                    else:
                        if judge_pure_english(text[i + j]):
                            word_count += len(segment_word(text[i + j]))
    frequency = word_count / (milliseconds / 60000)
    return word_count, milliseconds, frequency


def get_subtitle_filename_list(path, mode=''):
    filename_list = list()
    if mode == 'r':
        for root, dirs, files in os.walk(path, topdown=True):
            for file in files:
                filename = os.path.join(root, file)
                if '.srt' in filename:
                    filename_list.append(filename)
    else:
        for file in os.listdir(path):
            filename = os.path.join(path, file)
            if '.srt' in filename and not os.path.isdir(filename):
                filename_list.append(filename)

    return filename_list


def output_analysis_result_document(result_dict,
                                    filename='analysis_result.txt'):
    #todo split items of dict
    data = [result_dict[key] for key in result_dict.keys()]
    result_list = sorted(data, key=lambda x: x[3])
    with open(filename, 'w') as file:
        for result in result_list:
            file.writelines('%s\t%d\t%d\t%f\n' % (result[0], result[1],
                                                  result[2], result[3]))


def assign_tasks(filename_list, grain_size=1):
    task_list = [[
        filename_list[x * grain_size + y] for y in range(grain_size)
        if x * grain_size + y < len(filename_list)
    ] for x in range(math.ceil(len(filename_list) / grain_size))]
    return task_list


def execute_task_1(task_queue, result_queue):
    while True:
        try:
            filename_list = task_queue.get()
            result = result_queue.get()
            for filename in filename_list:
                frequency = read_subtitle_file(filename)
                result[filename] = frequency
            result_queue.put(result)
        finally:
            task_queue.task_done()
            result_queue.task_done()


def multithread_analyze_1(filename_list, max_workers=1, grain_size=1):
    task_list = assign_tasks(filename_list, grain_size)
    task_queue = queue.Queue()
    result_queue = queue.Queue()
    for task in task_list:
        task_queue.put(task)
    result_queue.put(dict())
    thread_list = [
        threading.Thread(
            target=execute_task_1, args=(
                task_queue,
                result_queue,
            )) for x in range(max_workers)
    ]
    for thread in thread_list:
        thread.daemon = True
        thread.start()
    try:
        task_queue.join()
    except KeyboardInterrupt:
        print("stopped by hand")
    while result_queue.empty() == False:
        return result_queue.get()
    return dict()


def single_thread_analyze(filename_list):
    result = dict()
    for filename in filename_list:
        try:
            word_count, milliseconds, frequency = read_subtitle_file(filename)
            result[filename] = [filename, word_count, milliseconds, frequency]
        except Exception as e:
            print(repr(e))
    return result


def test_multithread_analyze_1():
    filename_list = get_subtitle_filename_list('./srt')
    result_dict = multithread_analyze_1(
        filename_list, max_workers=2, grain_size=4)
    output_analysis_result_document(
        result_dict, filename='analysis_result.txt')


def test_single_thread_analyze():
    filename_list = get_subtitle_filename_list('/home/bigding/Code/advanced-programming-techniques/hw02/data/ignore_tmp/homework01', mode='r')
    result_dict = single_thread_analyze(filename_list)
    output_analysis_result_document(
        result_dict, filename='analysis_result.txt')


if __name__ == '__main__':

    # t = timeit.repeat(
    #     'test_multithread_analyze_1()',
    #     'from __main__ import test_multithread_analyze_1',
    #     number=20,
    #     repeat=1)
    # print('Average time : %f, Minimum time : %f' % (sum(t) / len(t), min(t)))

    # t = timeit.repeat(
    #     'test_single_thread_analyze()',
    #     'from __main__ import test_single_thread_analyze',
    #     number=1,
    #     repeat=1)
    # print('Average time : %f, Minimum time : %f' % (sum(t) / len(t), min(t)))
    test_single_thread_analyze()
    # read_subtitle_file('/home/bigding/Code/advanced-programming-techniques/hw02/data/ignore_tmp/homework01/lost4/Lost S04E10 720p BluRay x264-CtrlHD(ED2000.COM).srt')
    # bigdata = open('/home/bigding/Code/advanced-programming-techniques/hw02/data/ignore_tmp/homework01/237055.Arrow_S01_1080p_HDTV_X264_DIMENSION/Arrow.S01E01.Pilot.1080p.WEB-DL.DD5.1.H.264-ECI.srt','rb')
    # detector = chardet.UniversalDetector()
    # for line in bigdata.readlines():    
    #     detector.feed(line)    
    #     if detector.done:            
    #         break
    # detector.close()
    # bigdata.close()
    # print(detector.result)