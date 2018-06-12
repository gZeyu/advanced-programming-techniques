from django.http import HttpResponse
from air.utils import get_air_data, get_city_name_list
import pymysql
import json


def api(request):
    if request.method == 'GET':
        if ('city_name' in request.GET.keys()) and (
                'begin_date' in request.GET.keys()) and (
                    'end_date' in request.GET.keys()):
            city_name = request.GET['city_name']
            begin_date = request.GET['begin_date']
            end_date = request.GET['end_date']
            connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='1',
            db='dev',
            charset='utf8')
            try:
                air_data = get_air_data(connection, city_name, begin_date, end_date)
            finally:
                connection.close()
            response = HttpResponse(json.dumps(air_data))
            return response
        elif 'city_name_list' in request.GET.keys():
            connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='1',
            db='dev',
            charset='utf8')
            try:
                city_name_list = get_city_name_list(connection)
            finally:
                connection.close()
            response = HttpResponse(json.dumps(city_name_list))
            return response
        else:
            return HttpResponse('null')