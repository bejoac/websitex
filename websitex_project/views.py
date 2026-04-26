from django.http import HttpResponse
from django.shortcuts import render
from .models import Person
from django.middleware.csrf import get_token

def home(request):
    persons = Person.objects.all()
    return render(request, "home.html", {"persons": persons})

def add_user(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    
    if Person.objects.filter(email=email).exists():
        context = {"first_name": first_name, "last_name": last_name, "email": email, "mail_exists": True}
        return render(request, "form.html", context)

    Person.objects.create(first_name=first_name, last_name=last_name, email=email) # Does this throw an error?

    return HttpResponse("<p>Worked!</p>")
