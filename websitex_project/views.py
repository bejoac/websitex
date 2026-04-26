from django.http import HttpResponse
from django.shortcuts import render
from .models import Person
from django.middleware.csrf import get_token

def home(request):
    return render(request, "home.html")

def test(request):
    html = "<p>worked</p>"
    return HttpResponse(html)
