# -*- coding: utf-8 -*-
import os
import pymysql
import json
def transpose(matrix):
    return list(map(list,zip(*matrix)))

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
            data_in_hour = dict()
            for row in results:
                if row[0].strftime("%Y-%m-%d") not in data_in_hour.keys():
                    data_in_hour[row[0].strftime("%Y-%m-%d")] = list()
                record = [x for x in row[2:]]
                if sum([0 if x >= 0 else 1 for x in record]) == 0: # Filter invalid data
                    data_in_hour[row[0].strftime("%Y-%m-%d")].append(record)
            data_in_day = dict()
            for k, v in data_in_hour.items():
                data_in_day[k] = [round(sum(x)/len(x), 3) for x in transpose(v)]
            # data_in_day = sorted(data_in_day.items(), key=lambda data_in_day:data_in_day[0])
            # for item in data_in_day:
            #     print(item)
            print(json.dumps(data_in_day))
        connection.commit()
    finally:
        connection.close()
    

    