from django.contrib.auth.models import User, Group
from django.db import models
from core.models import Model


class Team(Model):
    group = models.OneToOneField(Group, primary_key=True, on_delete=models.CASCADE, verbose_name="Group Account")
    total_points = models.PositiveIntegerField(default=0, verbose_name="Points")
    
    def __str__(self):
        return self.group.name
    def adjust_points(self, points, transaction=None):
        points = int(points)
        if transaction == 'deduct':
            points = points * -1
        self.total_points = self.total_points + points
        if self.total_points < 0:
            self.total_points = 0
        self.save()
    
    class Meta:
        permissions = [('access_team', 'Can Access Teams')]


class Account(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    
    def _team(self):
        try:
            return self.user.groups.all()[0].team
        except:
            return None

def create_account(sender, instance, created, **kwargs):
    if created:
       profile, created = Account.objects.get_or_create(user=instance)

models.signals.post_save.connect(create_account, sender=User)