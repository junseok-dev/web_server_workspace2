from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    print(type(request)) # <class 'django.core.handlers.wsgi.WSGIRequest'>
    print(request) # <WSGIRequest: GET '/first/'>
    return HttpResponse('Hello django')

def helloworld(request):
    return HttpResponse('Hello world')