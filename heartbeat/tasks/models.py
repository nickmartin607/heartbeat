import datetime
from django.db import models
from django.utils import timezone
from core.models import Model
from heartbeat.teams.models import Team


class Task(Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Team")
    subject = models.CharField(max_length=100, verbose_name="Subject")
    status = models.BooleanField(default=False, verbose_name="Status")
    point_value = models.PositiveIntegerField(default=100, verbose_name="Point Value")
    completed = models.DateTimeField(blank=True, null=True, verbose_name="Completed")

    def __str__(self):
        return self.subject
    def toggle(self):
        if not self.status and timezone.now() < self.deadline:
            self.enabled = not self.enabled
            self.save()
    def complete(self):
        if not self.status:
            self.enabled = False
            self.status = True
            self.completed = timezone.now()
            self.save()
            self.team.adjust_points(self.point_value)
    
    class Meta:
        abstract = True
    
        
class Inject(Task):
    details = models.TextField(max_length=600, verbose_name="Details")
    available = models.DateTimeField(blank=True, null=True, verbose_name="Available")
    deadline = models.DateTimeField(blank=True, null=True, verbose_name="Deadline")
    
    def __init__(self, *args, **kwargs):
        kwargs['enabled'] = False
        super(Inject, self).__init__(*args, **kwargs)
    @classmethod
    def schedule(cls):
        for inject in cls.objects.all():
            if inject.enabled:
                if inject.deadline and timezone.now() > inject.deadline:
                    inject.toggle()
            else:
                if inject.available and timezone.now() > inject.available:
                    inject.toggle()
    
    
    class Meta:
        permissions = [('view_inject', 'Can view inject')]
    
        
class Action(Task):
    
    class Meta:
        permissions = [('view_action', 'Can view action')]
        

