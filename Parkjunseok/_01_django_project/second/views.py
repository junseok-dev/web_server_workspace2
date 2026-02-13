from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'second/index.html') # template폴더 기준 상대경로