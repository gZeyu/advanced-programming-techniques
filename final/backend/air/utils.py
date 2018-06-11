# -*- coding: utf-8 -*-
import os
import pymysql
import datetime


def transpose(matrix):
    return list(map(list, zip(*matrix)))


def get_date_list(begin_date, end_date):
    begin_date = datetime.datetime.strptime(begin_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    delta = (end_date - begin_date).days
    date_list = [(begin_date + datetime.timedelta(days=x)).strftime('%Y-%m-%d')
                 for x in range(delta + 1)]
    return date_list


def get_air_data(connection, city_name, begin_date, end_date):
    air_data = dict()

    with connection.cursor() as cursor:
        sql = '''SELECT * FROM `%s` where meas_time >= '%s' and meas_time <= '%s';'''
        cursor.execute(sql % (city_name, begin_date, end_date))
        results = cursor.fetchall()
        
        date_list = get_date_list(begin_date, end_date)
        data_in_hour = {date_list[i]: list() for i in range(len(date_list))}
        for row in results:
            record = [x for x in row[2:]]
            data_in_hour[row[0].strftime("%Y-%m-%d")].append(record)

        data_in_day = {date_list[i]: list() for i in range(len(date_list))}
        for k, v in data_in_hour.items():
            v = transpose(v)
            v = [list(filter(lambda x: x >= 0, y))
                 for y in v]  # Remove invalid value
            data_in_day[k] = [
                round(sum(x) / len(x), 3) if len(x) > 0 else None for x in v
            ]
        
        data_in_day = [data_in_day[k] for k in date_list]
        data_in_day = transpose(data_in_day)
        keys = [
            'aqi', 'pm2_5', 'pm2_5_24h', 'pm10', 'pm10_24h', 'so2', 'so2_24h',
            'no2', 'no2_24h', 'o3', 'o3_24h', 'o3_8h', 'o3_8h_24h', 'co',
            'co_24h'
        ]
        air_data = {keys[i]:data_in_day[i] for i in range(15)}
        air_data['city_name'] = city_name
        air_data['begin_date'] = begin_date
        air_data['end_date'] = end_date
    return air_data


if __name__ == '__main__':

    connection = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='1',
        db='dev',
        charset='utf8')
    try:
        air_data = get_air_data(connection, '北京', '2017-01-01', '2017-12-31')
    finally:
        connection.close()
