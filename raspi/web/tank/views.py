from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def tank(request):
    return render(request, 'tank/tank.html', {'title': 'Tank Page'})

def home(request):
    return render(request, 'tank/home.html', {'title': 'Home Page'})