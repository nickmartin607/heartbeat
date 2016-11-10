from django.conf.urls import url, include
from django.contrib import admin
from authentication import urls as auth_urls
from .views import *

system_urls = [
    url(r'^$',                          SystemList,                             name='all'),
]
host_urls = [
    url(r'^add$',                       HostAdd,                                name='add'),
    url(r'^delete/(?P<id>[0-9]+)$',     HostDelete,                             name='delete'),
    url(r'^modify/(?P<id>[0-9]+)$',     HostModify,                             name='modify'),
    url(r'^toggle/(?P<id>[0-9]+)$',     HostToggle,                             name='toggle'),
    url(r'^check/(?P<id>[0-9]+)$',      HostCheck,                              name='check'),
]
service_urls = [
    url(r'^add/(?P<hid>[0-9]+)$',       ServiceAdd,                             name='add'),
    url(r'^modify/(?P<id>[0-9]+)$',     ServiceModify,                          name='modify'),
    url(r'^delete/(?P<id>[0-9]+)$',     ServiceDelete,                          name='delete'),
    url(r'^toggle/(?P<id>[0-9]+)$',     ServiceToggle,                          name='toggle'),
    url(r'^check/(?P<id>[0-9]+)$',      ServiceCheck,                           name='check'),
]
inject_urls = [
    url(r'^$',                          InjectList,                             name='all'),
    url(r'^add$',                       InjectAdd,                              name='add'),
    url(r'^modify/(?P<id>[0-9]+)$',     InjectModify,                           name='modify'),
    url(r'^delete/(?P<id>[0-9]+)$',     InjectDelete,                           name='delete'),
    url(r'^toggle/(?P<id>[0-9]+)$',     InjectToggle,                           name='toggle'),
    url(r'complete/(?P<id>[0-9]+)$',    InjectComplete,                         name='complete'),
]
schedule_urls = [
    url(r'^toggle/$',                   ScheduleToggle,                         name='toggle'),
]

urlpatterns = [
    url(r'^$',                          Index,                                  name='index'),
    url(r'^systems/',                   include(system_urls,                    namespace='system')),
    url(r'^hosts/',                     include(host_urls,                      namespace='host')),
    url(r'^services/',                  include(service_urls,                   namespace='service')),
    url(r'^injects/',                   include(inject_urls,                    namespace='inject')),
    url(r'^schedule/',                  include(schedule_urls,                  namespace='schedule')),
    url(r'^',                           include(auth_urls)),
    url(r'^admin/',                     include(admin.site.urls)),
]