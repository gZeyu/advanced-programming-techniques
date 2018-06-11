from django.http import HttpResponse
from air.utils import get_air_data
import pymysql
import json
def api(request):
    if request.method == 'GET' :
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