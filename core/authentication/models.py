from django.contrib.auth.models import User
from django.db import models


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
        perm = '{}.{}_{}'.format(str(model.appname), action, str(model.modelname))
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