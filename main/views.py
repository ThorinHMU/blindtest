from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.utils.functional import SimpleLazyObject
from django.utils.timezone import now
import time
import os
import subprocess


def get_m3u8_duration_from_file(path):
    total_duration = 0.0
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("#EXTINF:"):
                duration_str = line.replace("#EXTINF:", "").split(',')[0]
                total_duration += float(duration_str)
    return total_duration


# Create your views here.
def index(request):
    return render(request, "index.html", context={})


def login_page(request: WSGIRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Identifiants invalides")
    return render(request, "login.html")


def logout_page(request: WSGIRequest):
    if request.user.is_authenticated:
        print("Connecté en tant que", request.user.username)
        logout(request)
    else:
        print("pas co")
    return render(request, "index.html")


def signup(request: WSGIRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists() or len(password) < 4:
            return render(request, "new_account.html")

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return render(request, "index.html")
    return render(request, "new_account.html")


start_timestamp = int(time.time() * 1000)


def video_view(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(ip, request.user.username if request.user else "")
    cwd = os.getcwd()
    duration = get_m3u8_duration_from_file(f'{cwd}\main\static\stream\playlist.m3u8')
    return render(request, 'test.html', {
        'video_url': '/static/stream/playlist.m3u8',
        'start_time': start_timestamp,
        'duration': int(duration*1000),
        "timestamp": int(now().timestamp())
    })

def horloge_view(request):
    return render(request, 'horloge.html', {
        'timestamp': int(now().timestamp())
    })
