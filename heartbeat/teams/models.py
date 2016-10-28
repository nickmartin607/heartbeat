from django.contrib.auth.models import User, Group
from django.db import models
from core.models import Model


class Team(Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='teams', verbose_name="Group Account")
    name = models.CharField(max_length=30, verbose_name="Name")
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
        permissions = [('view_team', 'Can view team')]


class Account(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    
    def _group(self):
        try:
            return self.user.groups.all()[0]
        except:
            return None
    def _team(self):
        try:
            return self._group().teams.all()[0]
        except:
            return None
            
    def has_perm(self, action, model, id=None):
        if self.user.is_staff or not action:
            return (True, '')
        perm = '{}.{}_{}'.format(str(model._appname()), action, str(model._modelname()))
        if not self.user.has_perm(perm):
            return (False, '404')
        try:
            item = model.objects.get(pk=id)
            if not item.enabled:
                return (False, '401')
            if item.team != self._team():
                return (False, '401')
        except:
            pass
        return (True, '')
        
    group = property(_group)
    team = property(_team)
            

def create_account(sender, instance, created, **kwargs):
    if created:
       profile, created = Account.objects.get_or_create(user=instance)

models.signals.post_save.connect(create_account, sender=User)