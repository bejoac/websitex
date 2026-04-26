from django.http import HttpResponse
from django.shortcuts import render
from .models import Person
from django.middleware.csrf import get_token

def home(request):
    persons = Person.objects.all()
    return render(request, "home.html", {"persons": persons})

def add_user(request):
    email = request.POST.get("email")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    print(email)

    if not email: # TODO: Shouldn't be possible to Submit without Email
        return HttpResponse("<p>Please specify E-mail</p>")
    
    if Person.objects.filter(email=email).exists():
        return HttpResponse("<p>User with specified Mail already exists!</p>")

    Person.objects.create(first_name=first_name, last_name=last_name, email=email) # Does this throw an error?

    return HttpResponse("<p>Worked!</p>")
