from django.shortcuts import render, redirect
from main.models import Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    context = {}
    context["messages"] = Message.objects.all()
    return render(request, "index.html", context=context)


def register_(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("/")

    return render(request, 'register.html')


def login_(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user=user)
            return redirect("/")
    return render(request, "login.html")


def logout_(request):
    logout(request)
    print(request.path)
    return redirect("/")

