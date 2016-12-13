from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    
    @property
    def group(self):
        try:
            return self.user.groups.all()[0]
        except:
            return None
    @property
    def team(self):
        try:
            return self.group.teams.all()[0]
        except:
            return None
        
    def has_perm(self, action, model, id=None):
        if not self.user.is_staff or action:
            perm = '{}.{}_{}'.format(
                model._meta.app_label, action, model._meta.model_name)
            if not self.user.has_perm(perm):
                raise Http404("Denied - Permission")
            try:
                item = model.objects.get(pk=id)
                if not item.visible:
                    raise Http404("Denied - Visibility")
                if item.team != self.team():
                    raise Http404("Denied - Ownership")
            except:
                pass
        return True
        

def create_account(sender, instance, created, **kwargs):
    if created:
       profile, created = Account.objects.get_or_create(user=instance)
models.signals.post_save.connect(create_account, sender=User)