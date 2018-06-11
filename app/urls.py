from django.conf.urls import url
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'date', views.date_actuelle),
    url(r'pari/(?P<phase>[A-Za-z0-9]*)', views.pari, name = 'pari'),
    url(r'^inscription/$', views.inscription, name='inscription'),
    url(r'^deconnect_gen$', auth_views.logout_then_login, name='deconnect_gen'),
    url(r'^connexion$', auth_views.login, {'template_name': 'app/connexion.html', 'redirect_field_name': '/app/pari'}),
    ]