from django.contrib import admin
from .models import Host, Service, Credential


admin.site.register(Host)
admin.site.register(Service)
admin.site.register(Credential)
