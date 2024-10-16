from django.contrib import admin
from .models import Member,Tank,SensorData,TimeProfile

# Register your models here.
admin.site.register(Member)
admin.site.register(Tank)
admin.site.register(SensorData)
admin.site.register(TimeProfile)