from django.db import models
from django.core.urlresolvers import reverse

class Model(models.Model):
    @classmethod
    def _appname(cls):
        return cls._meta.app_label
    @classmethod
    def _modelname(cls):
        return cls._meta.model_name
    @classmethod
    def _fieldname(cls, field):
        if field in cls._meta.get_all_field_names():
            return cls._meta.get_field(field).verbose_name
        else:
            return '?'
    @classmethod
    def _namespace(cls, action):
        namespace = '{}:{}'.format(cls._modelname(), action)
        return namespace
    @classmethod
    def _url(cls, action, args=[]):
        return reverse(cls._namespace(action), args=args)
    
    class Meta:
        abstract = True