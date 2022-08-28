from multiprocessing import context
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Message, Room

# Create your views here.

def index(request):
    rooms = Room.objects.all()
    context = {
        "rooms": rooms,
    }
    return render(request, 'chat/index.html', context)

def room(request, room_name):
    messages = Message.objects.filter(room__name=room_name)

    context = {
        'room_name': room_name,
        'messages': messages
    }

    return render(request, 'chat/room.html', context)

def loginUser(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    
    return render(request, 'chat/login.html')
