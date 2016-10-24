from django.conf.urls import url, patterns
from .views import *

urlpatterns = [
    url(r'^(?P<id>[0-9]+)/(?P<transaction>award|deduct)/(?P<points>[0-9]+)$',
                            AdjustPoints,                 name='adjust-points'),
    url(r'^(?P<id>[0-9]+)/perform_checks$',
                            PerformChecks,                name='perform-checks'),
]