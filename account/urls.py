"""EmailDelivery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .import views

urlpatterns = [
   url(r'^signup/', views.signup, name = 'signup'),
   url(r'^logout/$', views.logout, name = 'logout'),
   url(r'^confirm/(?P<purpose>[\w\-]+)/(?P<username>[\w\-]+)/(?P<userID>\d+)/(?P<code>\d+)/$', views.confirm, name = 'confirm'),
   url(r'^forgot-password/$', views.forgot_password, name = 'forgot_password'),
]
