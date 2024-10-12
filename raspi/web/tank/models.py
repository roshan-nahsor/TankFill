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
    
from django.utils import timezone

class SensorData(models.Model):
    tank=models.ForeignKey(Tank, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField()
    tank_status=models.CharField(max_length=30, null=True)
    
    def __str__(self):
        # return self.timestamp
        # return self.timestamp.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d %H:%M:%S")
        timestamp_local = self.timestamp.astimezone(timezone.get_current_timezone())
        
        # Get the day with ordinal suffix
        day = timestamp_local.strftime("%d")
        if 4 <= int(day) <= 20 or 24 <= int(day) <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][int(day) % 10 - 1]

        # Format the timestamp with the ordinal suffix
        formatted_timestamp = timestamp_local.strftime(f"%A %B {day}{suffix} %I:%M:%S %p")
        return formatted_timestamp

    
class TimeProfile(models.Model):
    time_id=models.ForeignKey(Tank, on_delete=models.CASCADE)
    time_start=models.TimeField()
    time_end=models.TimeField()