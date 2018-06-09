from django.conf.urls import url
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'date', views.date_actuelle),
    url(r'lister_phases', views.lister_phases, name='lister_phases'),
    url(r'pari/(?P<phase>[A-Za-z0-9]*)', views.pari, name = 'pari'),
    ]