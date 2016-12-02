from django.contrib import admin
from .models import *

class TeamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['name', 'group']}),
    ]
admin.site.register(Team, TeamAdmin)

class HostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['team', 'name']}),
        ('System',          {'fields': ['ip', 'hostname', 'os']}),
        ('Details',         {'fields': ['visible', 'status']}),
    ]
admin.site.register(Host, HostAdmin)
class ServiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['host', 'team']}),
        ('Service',         {'fields': ['protocol', 'port']}),
        ('Details',         {'fields': ['visible', 'point_value', 'status']}),
        (None,              {'fields': ['notes']}),
    ]
admin.site.register(Service, ServiceAdmin)

class InjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['team']}),
        ('Inject',          {'fields': ['subject', 'details', 'point_value',]}),
        ('Availability',    {'fields': ['available', 'deadline']}),
        ('Details',         {'fields': ['visible', 'completed', 'timestamp']}),
    ]
admin.site.register(Inject, InjectAdmin)
class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['team']}),
        ('Task',        {'fields': ['details', 'point_value']}),
        ('Details',     {'fields': ['completed', 'timestamp']}),
    ]
admin.site.register(Task, TaskAdmin)

class HostCheckAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['team', 'host']}),
        ('Check',       {'fields': ['point_value', 'timestamp', 'result', 'details']}),
    ]
admin.site.register(HostCheck, HostCheckAdmin)
class ServiceCheckAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['team', 'service']}),
        ('Check',       {'fields': ['point_value', 'timestamp', 'result', 'details']}),
    ]
admin.site.register(ServiceCheck, ServiceCheckAdmin)

admin.site.register(Configuration)
admin.site.register(Points)