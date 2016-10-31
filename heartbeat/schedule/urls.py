from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^start$',  Toggle,     {'state': 'start'},     name='start'),
    url(r'^stop$',   Toggle,     {'state': 'stop'},      name='stop'),
]