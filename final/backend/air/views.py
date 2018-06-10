from django.http import HttpResponse


def api(request):
    if request.method == 'GET' :
        data = request.GET['city'] + request.GET['start'] + request.GET['end'] 
        response = HttpResponse(data)
        return response