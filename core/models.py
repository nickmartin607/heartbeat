from django.db import models
from django.core.urlresolvers import reverse

class Model(models.Model):
    enabled = models.BooleanField(default=True, verbose_name="Enabled?")
    
    @classmethod
    def _appname(cls):
        return cls._meta.app_label
    @classmethod
    def _modelname(cls):
        return cls._meta.model_name
    @classmethod
    def fieldname(cls, field):
        if field in cls._meta.get_all_field_names():
            return cls._meta.get_field(field).verbose_name
        else:
            return '?'
    @classmethod
    def namespace(cls, action):
        return '{}:{}'.format(cls._modelname(), action)
    @classmethod
    def url(cls, action, args=[]):
        return reverse(cls.namespace(action), args=args)
        
    appname = property(_appname)
    modelname = property(_modelname)
    
    class Meta:
        abstract = True