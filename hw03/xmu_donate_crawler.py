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
from pyquery import PyQuery
import sqlite3


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
    while True:
        i = task_queue.get()
        if not download(i, i + 1):
            message_queue.put(i)
        task_queue.task_done()


def Multithread_download(task_list, max_workers=1):
    logger = logging.getLogger(__file__)
    task_queue = queue.Queue()
    message_queue = queue.Queue()
    for i in task_list:
        task_queue.put(i)
    for i in range(max_workers):
        thread = threading.Thread(
            target=work_fun, args=(
                task_queue,
                message_queue,
            ))
        thread.daemon = True
        thread.start()
    task_queue.join()
    logger.info('Download completed.')
    error_id = [message_queue.get() for i in range(message_queue.qsize())]
    logger.info('Error id : %s' % (str(error_id)))
    return error_id


def parse_html(filepath):
    html = PyQuery(filename=filepath)
    data = []
    for tr in html('#list').items('tr'):
        if tr.find('td'):
            record = []
            for td in tr.items('td'):
                record.append(td.text())
            data.append(record)
    return data


def get_html_list_from_dir(path):
    filename_list = []
    for file in os.listdir(path):
        filename = os.path.join(path, file)
        if '.html' in filename and not os.path.isdir(filename):
            filename_list.append(filename)
    return filename_list


def create_connection(database_filepath=':memory:'):
    connection = sqlite3.connect(database_filepath)
    return connection


def init_xmu_donate_database(connection):
    cursor = connection.cursor()
    cursor.execute(
        "create table donate(id integer primary key, "
        "time datetime, name varchar(50), department varchar(50), alumni_association varchar(50), project varchar(50), money decimal(30, 2))"
    )


def add_record(connection, record):
    cursor = connection.cursor()
    sql = 'insert into donate values (null, "%s", "%s", "%s", "%s", "%s", %f)' % (
        record[0], record[1], record[2], record[3], record[4],
        float(record[5]))
    cursor.execute(sql)


def save_xmu_donate_data(connection, data):
    cursor = connection.cursor()
    for record in data:
        add_record(connection, record)


if __name__ == '__main__':
    init_logger()
    logger = logging.getLogger(__file__)

    # Download pages.
    # task_list = list(range(2001, 2120))
    # while task_list:
    #     task_list = Multithread_download(task_list, max_workers=2)

    filename_list = get_html_list_from_dir('./html')
    data = []
    for filename in filename_list:
        data.extend(parse_html(filename))

    connection = create_connection()
    init_xmu_donate_database(connection)
    save_xmu_donate_data(connection, data)

    cursor = connection.cursor()
    for row in cursor.execute('select * FROM donate'):
        print(row)
    connection.close()