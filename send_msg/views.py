from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime
from .forms import SendMessageModelForm

import logging

logger = logging.getLogger(__name__)

# Create your views here.

# Send message view
@login_required(login_url='/login/')
def send_msg(request):
    
    form = None

    if request.method == 'POST':
        
        form = SendMessageModelForm(request.POST)
        
        if form.is_valid():
            
            user = request.user
            
            msg = form.save(commit=False)
            msg.date = datetime.datetime.now()
            msg.sender = user

            sender_mail = user.email if user.email else f'{user.username}@no.email.com'

            try:
                send_mail('SendMessage', msg.text, sender_mail, [msg.receiver], fail_silently=False)
            except OSError:
                # Some speciefic actions here?
                # like writing to field error's message ?
                msg.success = False
            except Exception:
                msg.success = False
            else:
                msg.success = True

            msg.save()
            
            # logger.info('#################################')

            # TODO render some info about successed sending ? 
            return HttpResponseRedirect(reverse('sendmsg'))
    else:
        form = SendMessageModelForm()

    return render(request, 'send-message.html', {'form': form})