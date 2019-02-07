"""fogstream_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from site_auth import views as site_auth_views
from send_msg import views as send_msg_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # TODO replace LoginView bellow to class with logoutrequiredmixin?
    # more there https://stackoverflow.com/questions/38274769/what-is-the-opposite-of-loginrequiredmixin-how-deny-the-access-to-a-logged-in-u
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', site_auth_views.register, name='register'),
    path('send-message/', send_msg_views.send_msg, name='sendmsg'),
]
