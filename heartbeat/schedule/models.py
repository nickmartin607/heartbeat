import datetime, os, random, time, threading
from django.db import models
from django.utils import timezone
from core.models import Model
from heartbeat.systems.models import Service
from heartbeat.tasks.models import Inject

def get_schedule():
    try:
        return Schedule.objects.get(pk=1)
    except:
        return Schedule()

class Schedule(Model):
    period_fixed = models.PositiveIntegerField(default=60, verbose_name="Fixed Checking Period, in Seconds")
    period_min = models.PositiveIntegerField(default=5, verbose_name="Minimum Checking Period, in Seconds")
    period_max = models.PositiveIntegerField(default=15, verbose_name="Maximum Checking Period, in Seconds")
    
    def toggle(self, action):
        if action == 'start' and not self.enabled:
            self.enabled = True
            self.save()
            self.execute()
        else:
            self.enabled = False
            self.save()
    
    def sleep(self, rand=True):
        time.sleep(random.randint(self.period_min, self.period_max) if rand else self.period_fixed)
        
    def execute(self):
        t1 = threading.Thread(target=self.service_checks)
        t2 = threading.Thread(target=self.general_tasks)
        t1.start()
        t2.start()
    
    def service_checks(self):
        while True:
            print(' > Looping Service Checks')
            self.sleep(rand=True)
            Service.schedule()
            self.refresh_from_db()
            if not self.enabled:
                break
            
    def general_tasks(self):
        while True:
            print(' > Looping General Tasks')
            self.sleep()
            Inject.schedule()
            self.refresh_from_db()
            if not self.enabled:
                break