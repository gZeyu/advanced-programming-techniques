# -*- coding: utf-8 -*-
import sys
import os
# import traceback
import logging
import datetime
from urllib import (request, error)


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
    except error.URLError as e:
        logger.error(e.reason)

    return html


def save_html(str, filepath):
    with open(filepath, 'w') as file:
        file.write(str)


def download(num=10):
    logger = logging.getLogger(__file__)
    for i in range(1, num + 1):
        html = get_html('http://edf.xmu.edu.cn/Donate?page=%d' % (i))
        if html != None:
            save_html(html.read().decode('utf-8'),
                      os.path.join('html', 'page%d.html' % (i)))
            logger.debug('Downloaded Page %d successfully' % (i))


#todo read_html

if __name__ == '__main__':
    pass
    init_logger()
    download(2114)
