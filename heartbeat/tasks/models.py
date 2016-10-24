from django.db import models
from django.utils import timezone
from core.models import Model
from heartbeat.teams.models import Team


class Task(Model):
    subject = models.CharField(max_length=100, verbose_name="Subject")
    status = models.BooleanField(default=False, verbose_name="Status")
    point_value = models.PositiveIntegerField(default=100, verbose_name="Point Value")
    completed = models.DateTimeField(blank=True, null=True, verbose_name="Completed")

    def __str__(self):
        return self.subject
    def complete(self):
        self.status = True
        self.completed = timezone.now()
        self.team.adjust_points(self.point_value)
        super(Task, self).save()
    
    class Meta:
        abstract = True
    
        
class Inject(Task):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='injects', related_query_name='inject', verbose_name="Team")
    details = models.TextField(max_length=600, verbose_name="Details")
    enabled = models.BooleanField(default=False, verbose_name="Enabled?")
    available = models.DateTimeField(blank=True, null=True, verbose_name="Available")
    deadline = models.DateTimeField(blank=True, null=True, verbose_name="Deadline")
    
    def complete(self):
        if not self.status:
            super(Inject, self).complete()
            self.enabled = False
            self.save()
    def toggle(self):
        if not self.status:
            self.enabled = not self.enabled
            self.save()
    def can_view(self, user):
        if user.account._team() == self.team:
            if self.enabled:
                return True
        return False
    
    class Meta:
        permissions = [('access_inject', 'Can Access Injects')]
    
        
class Action(Task):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='actions', related_query_name='action', verbose_name="Team")
    
    def save(self, *args, **kwargs):
        super(Action, self).save(*args, **kwargs)
        self.complete()
    
    class Meta:
        permissions = [('access_action', 'Can Access Actions')]
        

