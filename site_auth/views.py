from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse


def is_user_not_logged_in(user):
    return not user.is_authenticated

# Create your views here.
@user_passes_test(is_user_not_logged_in, login_url='/send-message/', redirect_field_name=None)
def register(request):

    # if POST - processing a form
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            rawpass = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=rawpass)
            login(request,user)
            return redirect('sendmsg')

    # not POST - just create a form
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
