from django.http import HttpResponse
from django.shortcuts import render
from .models import Entry

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "home.html")

@login_required(login_url="/")
def user_space(request):
    entries = Entry.objects.filter(user=request.user)
    return render(request, "user_space.html", {"entries": entries})


def register_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    if User.objects.filter(username=username).exists():
        return HttpResponse("Username already taken!", status=422)
    
    try:
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        response = HttpResponse()
        response["HX-Redirect"] = "/user_space/"
        return response
    except Exception as e:
        return HttpResponse(f"Failed: {str(e)}", status=500)
    

def login_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        response = HttpResponse()
        response["HX-Redirect"] = "/user_space/"
        return response
    else:
        error = "Failed to authenticate user"
        return render(request, "login_user.html", context={"error": error}, status=422)

def get_login_form(request):
    return render(request, "login_user.html")


def get_register_form(request):
    return render(request, "register_user.html")


@login_required(login_url="/")
def logout_user(request):
    logout(request)
    reponse = HttpResponse()
    reponse["HX-Redirect"] = "/"
    return reponse


@login_required(login_url="/")
def delete_user(request):
    user_to_delete = User.objects.filter(username=request.user)
    user_to_delete.delete()
    response = HttpResponse()
    response["HX-Redirect"] = "/"
    return response


def delete_entry(request, id):
    entry_to_delete = Entry.objects.filter(user=request.user, id=id)
    entry_to_delete.delete()
    return HttpResponse("")


def add_entry(request):
    user_entry = request.POST.get("user_entry")
    user_entry_object = Entry.objects.create(user=request.user, user_entry=user_entry)
    return render(request, "oob_entry.html", {"entry": user_entry_object})


def get_edit_form(request, id):
    return render(request, "edit_entry.html", {"id": id})

def edit_entry(request, id):
    entry = Entry.objects.get(user=request.user, id=id)
    return render(request, "entry.html", {"entry": entry})