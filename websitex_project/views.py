from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Person
from django.middleware.csrf import get_token

from django.template.loader import render_to_string

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

    Person.objects.create(first_name=first_name, last_name=last_name, email=email)

    form_html = render_to_string("form.html", {}, request=request)
    contact_html = render_to_string("oob_contact.html", {"first_name": first_name, "last_name": last_name}, request=request)

    return HttpResponse(form_html + contact_html)

def get_users(request):
    persons = Person.objects.all()
    return render(request, "listing_persons.html", {"persons": persons})

def delete_user(request, id):
    print(id)
    return HttpResponse("")