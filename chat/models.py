from statistics import mode
from django.db import models

# Create your models here.

class Message(models.Model):
    body = models.TextField(max_length=200, null=True, blank=True)
    room = models.TextField(max_length=100, null=True, blank=True)