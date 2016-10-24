from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^$',          'heartbeat.views.Index',                name='index'),
    url(r'^teams/',     include('heartbeat.teams.urls',         namespace='team')),
    url(r'^systems/',   include('heartbeat.systems.urls')),
    url(r'^checks/',    include('heartbeat.checks.urls')),
    url(r'^',           include('heartbeat.tasks.urls')),
    url(r'^',           include('core.auth.urls')),
    url(r'^admin/',     include(admin.site.urls)),
]