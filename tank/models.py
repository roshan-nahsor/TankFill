from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Member(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    
    # help_text="Use make_password to hash the password before saving."
    password=models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return raw_password == self.password
    
    def __str__(self):
        return self.fname+' '+self.lname

class Tank(models.Model):
    name=models.CharField(max_length=50)
    height=models.IntegerField()
    upper_limit=models.IntegerField()
    lower_threshold=models.IntegerField()
    # subscribe_topic=models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
class SensorData(models.Model):
    tank=models.ForeignKey(Tank, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField()
    
class TimeProfile(models.Model):
    time_id=models.ForeignKey(Tank, on_delete=models.CASCADE)
    time_start=models.TimeField()
    time_end=models.TimeField()