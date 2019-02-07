from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    text = models.TextField(max_length=1000, help_text='Write your message here')
    receiver = models.EmailField(max_length=256)
    success = models.BooleanField(default=False)
    date = models.DateTimeField("Send date", auto_now=False, auto_now_add=False)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
