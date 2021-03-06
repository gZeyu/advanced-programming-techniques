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
import traceback


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
    milliseconds = 0
    word_count = 0
    file = open(filename, "rb")
    detector = chardet.UniversalDetector()
    filelines = len(file.readlines())
    threshold = 50
    file.seek(0)
    n = filelines if filelines < threshold else threshold
    for line in file.readlines()[0:n]:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    file.close()
    with open(
            filename, 'r', encoding=detector.result['encoding'],
            errors='ignore') as file:
        text = file.readlines()
        filelines = len(text)
        for i in range(filelines):
            if '-->' in text[i]:
                text[i] = text[i].replace('-->', ' --> ')
                elements = text[i].split()
                try:
                    milliseconds += format_time(elements[2]) - format_time(
                        elements[0])
                except:
                    break
                for j in range(1, 2):
                    if i + j >= filelines:
                        break
                    if text[i + j].strip() == '':
                        break
                    else:
                        if judge_pure_english(text[i + j]):
                            try:
                                word_count += len(segment_word(text[i + j]))
                            except:
                                break
    frequency = word_count / (milliseconds / 60000)
    return word_count, milliseconds, frequency


def get_subtitle_filename_list(path, mode=''):
    filename_list = list()
    if mode == 'r':
        for root, _, files in os.walk(path, topdown=True):
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
                                                  result[2] / 1000, result[3]))


def assign_tasks(filename_list, grain_size=1):
    task_list = [[
        filename_list[x * grain_size + y] for y in range(grain_size)
        if x * grain_size + y < len(filename_list)
    ] for x in range(math.ceil(len(filename_list) / grain_size))]
    return task_list


def execute_task(task_queue, result_queue):
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


def multithread_analyze(filename_list, max_workers=1, grain_size=1):
    task_list = assign_tasks(filename_list, grain_size)
    task_queue = queue.Queue()
    result_queue = queue.Queue()
    for task in task_list:
        task_queue.put(task)
    result_queue.put(dict())
    thread_list = [
        threading.Thread(
            target=execute_task, args=(
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
    errors_filename = 'errors.log'
    count = 0
    with open(errors_filename, 'w') as file:
        for filename in filename_list:
            # word_count, milliseconds, frequency = read_subtitle_file(filename)
            # result[filename] = [filename, word_count, milliseconds, frequency]
            try:
                word_count, milliseconds, frequency = read_subtitle_file(
                    filename)
                result[filename] = [
                    filename, word_count, milliseconds, frequency
                ]
            except Exception:
                file.writelines('[%d]' % (count) + traceback.format_exc() +
                                'filename: %s\n\n' % (filename))
                count = count + 1
    return result


def test_multithread_analyze():
    filename_list = get_subtitle_filename_list('./srt')
    result_dict = multithread_analyze(
        filename_list, max_workers=2, grain_size=4)
    output_analysis_result_document(
        result_dict, filename='analysis_result.txt')


def test_single_thread_analyze():
    filename_list = get_subtitle_filename_list(
        '/home/bigding/Code/advanced-programming-techniques/hw02/data/ignore_tmp/homework01',
        mode='r')
    result_dict = single_thread_analyze(filename_list)
    output_analysis_result_document(
        result_dict, filename='analysis_result.txt')


if __name__ == '__main__':

    # t = timeit.repeat(
    #     'test_multithread_analyze()',
    #     'from __main__ import test_multithread_analyze',
    #     number=20,
    #     repeat=1)
    # print('Average time : %f, Minimum time : %f' % (sum(t) / len(t), min(t)))

    # t = timeit.repeat(
    #     'test_single_thread_analyze()',
    #     'from __main__ import test_single_thread_analyze',
    #     number=1,
    #     repeat=1)
    # print('Average time : %f, Minimum time : %f' % (sum(t) / len(t), min(t)))
    start = time.time()

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = 'ignore_tmp/test'
    if len(sys.argv) > 2:
        filename = sys.argv[2]
    else:
        filename = 'analysis_result.txt'

    filename_list = get_subtitle_filename_list(path, mode='r')
    print("Found: %d subtitles" % (len(filename_list)))
    result_dict = single_thread_analyze(filename_list)
    output_analysis_result_document(result_dict, filename=filename)
    end = time.time()
    print("Elapsed: %.03f seconds" % (end - start))
