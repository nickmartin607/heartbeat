from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^login$',     Login,      name='login'),
    url(r'^logout$',    Logout,     name='logout'),
    url(r'^passwd$',    Passwd,     name='passwd'),
    url(r'^401',        Error401,   name='401'),
    url(r'^404',        Error404,   name='404'),
]