# -*- coding: utf-8 -*-
import sys
import os
import traceback
import logging
import datetime
from urllib import (request, error)
import queue
import threading


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
        html = request.urlopen(url, timeout=3)
    except Exception:
        logger.error(traceback.format_exc())

    return html


def save_html(str, filepath):
    with open(filepath, 'w') as file:
        file.write(str)


def download(start=1, stop=10):
    logger = logging.getLogger(__file__)
    for i in range(start, stop + 1):
        html = get_html('http://edf.xmu.edu.cn/Donate?page=%d' % (i))
        if html != None:
            save_html(html.read().decode('utf-8'),
                      os.path.join('html', 'page%d.html' % (i)))
            # logger.debug('Downloaded Page %d successfully.' % (i))
            logger.info('[%s]Downloaded Page %d successfully.' %
                        (threading.current_thread().getName(), i))


def work_fun(task_queue):
    logger = logging.getLogger(__file__)
    while True:
        i = task_queue.get()
        download(i, i + 1)
        # logger.info('[%s]Downloaded Page %d successfully.' %
        #             (threading.current_thread().getName(), i))
        task_queue.task_done()


def Multithread_download(total_page_number=10, max_workers=1):
    logger = logging.getLogger(__file__)
    task_queue = queue.Queue()
    for i in range(1, total_page_number + 1):
        task_queue.put(i)
    for i in range(max_workers):
        thread = threading.Thread(target=work_fun, args=(task_queue, ))
        thread.daemon = True
        thread.start()
    task_queue.join()
    logger.info('Download completed.')


if __name__ == '__main__':
    init_logger()
    Multithread_download(total_page_number=2119, max_workers=4)
