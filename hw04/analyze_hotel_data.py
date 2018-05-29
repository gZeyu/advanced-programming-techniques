# -*- coding: utf-8 -*-

# import pymysql
 
# # 打开数据库连接
# db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='hotel', charset='utf8')
 
# # 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()
 
# # 使用 execute()  方法执行 SQL 查询 
# cursor.execute("SELECT VERSION()")
 
# # 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()
 
# print ("Database version : %s " % data)
 
# # 关闭数据库连接
# db.close()

import time
import sys

from pyecharts import Pie, Bar, WordCloud, Page

def create_charts():
    page = Page()

    attr = ["男性", "女性", "无性别"]
    gender = [12773970, 6479097, 797077]
    chart = Pie("性别", title_pos='center')
    chart.add("", attr, gender, is_label_show=True)
    page.add(chart)

    attr = ["50后", "60后", "70后", "80后", "90后", "其他"]
    age = [971253, 2758022, 5078234, 7395064, 1514256, 945754]
    chart = Bar("性别", title_pos='center')
    chart.add("", attr, age, is_stack=True)
    page.add(chart)

    attr = ["@qq.com"," @163.com", "@126.com", "@hotmail.com", "@sina.com",
            "@yahoo.com.cn", "@gmail.com", "@139.com", "@sohu.com", "@yahoo.cn"]
    email = [611842, 594392, 274512, 203237, 151798, 101692, 96346, 67565, 50179, 31274]
    chart = Pie("Top10 邮箱域名", title_pos='center')
    chart.add("", attr, email, is_random=True,
              radius=[20, 80], rosetype='radius', legend_orient='vertical', 
              legend_pos='left')
    page.add(chart)
    return page

if __name__=="__main__":

    create_charts().render()
