# -*- coding: utf-8 -*-
import os
import pymysql
import json
import datetime
def transpose(matrix):
    return list(map(list,zip(*matrix)))
def get_date_list(begin_date, end_date):
    begin_date = datetime.datetime.strptime(begin_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    delta = (end_date-begin_date).days
    date_list = [(begin_date+datetime.timedelta(days=x)).strftime('%Y-%m-%d') for x in range(delta+1)]
    return date_list
if __name__ == '__main__':

    connection = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='1',
        db='dev',
        charset='utf8')
    try:
        with connection.cursor() as cursor:
            # """ rename """
            # sql = '''select table_name 
            #          from information_schema.tables 
            #          where table_schema='dev';'''
            # cursor.execute(sql)
            # results = cursor.fetchall()   
            # for item in results:
            #     table_name = item[0]
            #     city_name = table_name.split('_')[0]
            #     new_table_name = city_name + ''
            #     sql = '''alter table `%s` rename `%s`;''' % (table_name, new_table_name)
            #     cursor.execute(sql)
            sql = '''select * from 北京'''
            cursor.execute(sql)
            results = cursor.fetchall()

            date_list = get_date_list('2017-01-01', '2017-12-31')
            data_in_hour = {date_list[i]:list() for i in range(len(date_list))}
            for row in results:
                record = [x for x in row[2:]]
                data_in_hour[row[0].strftime("%Y-%m-%d")].append(record)
            
            data_in_day = {date_list[i]:list() for i in range(len(date_list))}
            for k, v in data_in_hour.items():
                v = transpose(v)
                v = [list(filter(lambda x:x>=0, y)) for y in v] # Remove invalid value
                data_in_day[k] = [round(sum(x)/len(x), 3) if len(x)>0 else None for x in v]
        connection.commit()
    finally:
        connection.close()
    

    