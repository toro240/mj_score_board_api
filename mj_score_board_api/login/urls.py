from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'login'
urlpatterns = [
    path('auth', csrf_exempt(views.auth), name='auth'),
    path('new', csrf_exempt(views.new), name='new'),
]
