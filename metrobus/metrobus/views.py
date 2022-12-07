from django.http import HttpResponse

def index(request):    
    return HttpResponse('API para la consulta de estaciones del metrobus dentro de la Ciudad de México.')
