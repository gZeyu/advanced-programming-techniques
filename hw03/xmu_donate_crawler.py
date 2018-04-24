# -*- coding: utf-8 -*-
import sys
import os
import traceback
import logging
import datetime
from urllib import (request, error)
import queue
import threading
import time


def init_logger():
    logger = logging.getLogger(__file__)
    logger.setLevel(level=logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

    log_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    handler = logging.FileHandler(log_name + '.log')
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console)


def get_html(url):
    logger = logging.getLogger(__file__)
    html = None
    try:
        html = request.urlopen(url, timeout=5)
    except Exception:
        logger.error(traceback.format_exc())

    return html


def save_html(str, filepath):
    with open(filepath, 'w') as file:
        file.write(str)


def download(start=1, stop=10):
    logger = logging.getLogger(__file__)
    for i in range(start, stop):
        html = get_html('http://edf.xmu.edu.cn/Donate?page=%d' % (i))
        if html != None:
            save_html(html.read().decode('utf-8'),
                      os.path.join('html', 'page%d.html' % (i)))
            # logger.debug('Downloaded Page %d successfully.' % (i))
            logger.info('[%s]Downloaded Page %d successfully.' %
                        (threading.current_thread().getName(), i))
            return True
        else:
            return False


def work_fun(task_queue, message_queue):
    logger = logging.getLogger(__file__)
    while True:
        i = task_queue.get()
        if not download(i, i + 1):
            message_queue.put(i)
        # time.sleep(1)
        # logger.info('[%s]Downloaded Page %d successfully.' %
        #             (threading.current_thread().getName(), i))
        task_queue.task_done()


def Multithread_download(task_list, max_workers=1):
    logger = logging.getLogger(__file__)
    task_queue = queue.Queue()
    message_queue = queue.Queue()
    for i in task_list:
        task_queue.put(i)
    for i in range(max_workers):
        thread = threading.Thread(target=work_fun, args=(task_queue, message_queue, ))
        thread.daemon = True
        thread.start()
    task_queue.join()
    logger.info('Download completed.')
    error_id = [message_queue.get() for i in range(message_queue.qsize())]
    logger.info('Error id : %s'%(str(error_id)))
    return error_id

if __name__ == '__main__':
    init_logger()
    task_list = list(range(2001, 2120))
    while task_list:
        task_list = Multithread_download(task_list, max_workers=2)
    
