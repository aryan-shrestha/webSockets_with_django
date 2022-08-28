from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.TextField(max_length=100, null=True, blank=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(max_length=200, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)