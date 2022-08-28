
from django.shortcuts import render
from django.http import JsonResponse

from .models import Message

# Create your views here.

def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    messages = Message.objects.filter(room=room_name)

    context = {
        'room_name': room_name,
        'messages': messages
    }

    return render(request, 'chat/room.html', context)
