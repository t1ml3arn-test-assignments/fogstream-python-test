from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Message(models.Model):
    text = models.TextField(max_length=1000, help_text='Write your message here')
    receiver = models.EmailField(max_length=254)
    success = models.BooleanField(default=False)
    date = models.DateTimeField("Send date", default=datetime.now)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
