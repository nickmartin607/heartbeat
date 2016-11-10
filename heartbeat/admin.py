from django.contrib import admin
from .models import *


class TeamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['name', 'group']}),
    ]
class HostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['team', 'name']}),
        ('System',      {'fields': ['ip', 'hostname', 'os']}),
        ('Details',     {'fields': ['visible', 'details']}),
    ]
class ServiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['host']}),
        ('Service',     {'fields': ['protocol', 'port']}),
        ('Details',     {'fields': ['visible', 'point_value', 'details']}),
    ]
class InjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['team']}),
        ('Inject',      {'fields': ['subject', 'details', 'point_value']}),
        ('Events',      {'fields': ['available', 'deadline']}),
        ('Details',     {'fields': ['visible', 'status']}),
    ]
class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['team']}),
        ('Task',        {'fields': ['subject', 'point_value']}),
    ]
class CheckAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['team', 'timestamp']}),
        ('Check',       {'fields': ['host', 'service']}),
        ('Results',     {'fields': ['status', 'details']}),
    ]
class CredentialAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['name']}),
        ('Credentials', {'fields': ['username', 'password']}),
    ]

admin.site.register(Team, TeamAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Inject, InjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Check, CheckAdmin)
admin.site.register(Credential, CredentialAdmin)
admin.site.register(Schedule)