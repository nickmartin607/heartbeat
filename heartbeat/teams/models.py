from django.contrib.auth.models import Group
from django.db import models
from core.models import Model


class Team(Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='teams', verbose_name="Group Account")
    name = models.CharField(max_length=30, verbose_name="Name")
    total_points = models.PositiveIntegerField(default=0, verbose_name="Points")
    
    def __str__(self):
        return self.name
    def adjust_points(self, points, transaction=None):
        points = int(points)
        if transaction == 'deduct':
            points = points * -1
        self.total_points = self.total_points + points
        if self.total_points < 0:
            self.total_points = 0
        self.save()
    
    class Meta:
        permissions = [('view_team', 'Can view team')]
