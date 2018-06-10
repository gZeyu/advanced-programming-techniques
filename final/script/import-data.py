# -*- coding: utf-8 -*-
import os
import csv
import pymysql

AIR_QUALITY_DATA_DIR = '../air-data/城市_20170101-20171231'


def get_data_filename_list(path):
    filename_list = []
    for file in os.listdir(path):
        filename = os.path.join(path, file)
        if '.csv' in filename and not os.path.isdir(filename):
            filename_list.append(filename)
    return filename_list


def read_data_file(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        data = list(spamreader)
        return data


def reshape_data(origin_data):
    city_name_list = (origin_data[0])[3:len(origin_data[0])]
    data = dict()
    rows = int((len(origin_data) - 1) / 15)
    for i in range(len(city_name_list)):
        city_data = list()
        for j in range(rows):
            city_data.append(
                origin_data[j * 15 + 1][0:2] +
                [origin_data[j * 15 + k + 1][i + 3] for k in range(15)])
        data[city_name_list[i]] = city_data
    return data


def save_data_to_mysql(connection, table_suffix, data):
    try:
        with connection.cursor() as cursor:
            city_name_list = data.keys()
            for city_name in city_name_list:
                sql = '''CREATE TABLE IF NOT EXISTS `%s` (
                        `meas_time` DATE NOT NULL,
                        `meas_hour` TINYINT NOT NULL,
                        `aqi` FLOAT NOT NULL,
                        `pm2_5` FLOAT NOT NULL,
                        `pm2_5_24h` FLOAT NOT NULL,
                        `pm10` FLOAT NOT NULL,
                        `pm10_24h` FLOAT NOT NULL,
                        `so2` FLOAT NOT NULL,
                        `so2_24h` FLOAT NOT NULL,
                        `no2` FLOAT NOT NULL,
                        `no2_24h` FLOAT NOT NULL,
                        `o3` FLOAT NOT NULL,
                        `o3_24h` FLOAT NOT NULL,
                        `o3_8h` FLOAT NOT NULL,
                        `o3_8h_24h` FLOAT NOT NULL,
                        `co` FLOAT NOT NULL,
                        `co_24h` FLOAT NOT NULL
                        );''' % (city_name+table_suffix)
                cursor.execute(sql)

                sql = 'INSERT INTO `' + city_name+table_suffix \
                    + '` VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                # cursor.executemany(sql, data[city_name])
                for row in data[city_name]:
                    # print(sql % (tuple([x if len(x) > 0 else '-9999' for x in row])))
                    cursor.execute(sql % (tuple([x if len(x) > 0 else '-99999' for x in row])))
            # pass
        connection.commit()
    finally:
        return


if __name__ == '__main__':

    filename_list = get_data_filename_list(AIR_QUALITY_DATA_DIR)
    # for filename in filename_list:
    #     print(filename)
    connection = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='1',
        db='django_test',
        charset='utf8')
    table_suffix = '_20170101_20171231'
    filename_list.sort()
    for filename in filename_list[0:3]:
        origin_data = read_data_file(filename)
        data = reshape_data(origin_data)
        save_data_to_mysql(connection, table_suffix, data)
        print(filename)
    print('done!')
    connection.close()