from django.db import models
    
class Model(models.Model):
    visible = models.BooleanField(default=True, verbose_name="Visible?")
    
    def toggle(self):
        self.visible = not self.visible
        self.save()
    
    class Meta:
        abstract = True