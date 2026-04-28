from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Person
from django.middleware.csrf import get_token
import time
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, login_not_required

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

    person = Person.objects.create(first_name=first_name, last_name=last_name, email=email)

    form_html = render_to_string("form.html", {}, request=request)
    contact_html = render_to_string("oob_contact.html", {"person": person}, request=request)

    return HttpResponse(form_html + contact_html)

def delete_user(request, id):
    person_to_delete = Person.objects.filter(id=id)
    person_to_delete.delete()
    time.sleep(2)
    return HttpResponse("")

def register_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    if User.objects.filter(username=username).exists():
        return HttpResponse("Username already taken!", status=422)
    
    try:
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return HttpResponse("User registered and logged in!")
    except Exception as e:
        return HttpResponse(f"Failed: {str(e)}", status=500)

def login_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        return render(request, "home.html")
    else:
        return HttpResponse("Failed to log in!")

def get_login_form(request):
    return render(request, "login_user.html")

def get_register_form(request):
    return render(request, "register_user.html")

@login_required(login_url="/")
def logout_user(request):
    logout(request)
    return render(request, "home.html")