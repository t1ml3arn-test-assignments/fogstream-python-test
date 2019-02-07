from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from send_msg.models import Message

import logging

logger = logging.getLogger(__name__)


class SendMessageModelForm(ModelForm):

    def clean_receiver(self):

        data = self.cleaned_data.get("receiver")
        
        try:
            User.objects.get(email=data)
        except User.DoesNotExist:
            raise ValidationError(f'There are no admins with email {data}')
        
        return data

    class Meta:
        model = Message
        fields = ["receiver", "text"]
        labels = {"receiver": "Admin's email", "text": "Message"}