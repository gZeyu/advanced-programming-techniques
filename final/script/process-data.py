# -*- coding: utf-8 -*-
import os
import csv
import pymysql

AIR_QUALITY_DATA_DIR = '../air-quality-data/城市_20150101-20151231'


def get_air_quality_data_filename_list(path):
    filename_list = []
    for file in os.listdir(path):
        filename = os.path.join(path, file)
        if '.csv' in filename and not os.path.isdir(filename):
            filename_list.append(filename)
    return filename_list


def read_air_quality_data_file(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))


if __name__ == '__main__':

    filename_list = get_air_quality_data_filename_list(AIR_QUALITY_DATA_DIR)
    # for filename in filename_list:
    #     print(filename)
    read_air_quality_data_file(filename_list[0])
    # db = pymysql.connect("localhost", "root", "123456", "dev")
    # cursor = db.cursor()
    # cursor.execute("SELECT VERSION()")
    # data = cursor.fetchone()
    # print("Database version : %s " % data)
    # db.close()