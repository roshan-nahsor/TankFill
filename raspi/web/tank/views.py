from django.shortcuts import render
# from django.http import HttpResponse
from .models import Tank, SensorData, TimeProfile
from .forms import TankForm, TimeForm

import paho.mqtt.publish as publish
import json

# Create your views here.
def tank(request):
    return render(request, 'tank/tank.html', {'title': 'Tank Page'})

def home(request):
    tank=Tank.objects.first()
    time_profile=TimeProfile.objects.first()
    if request.method=="POST":
        tank_form=TankForm(request.POST, instance=tank)
        time_profile_form = TimeForm(request.POST, instance=time_profile)
        h=int(request.POST.get('height'))
        ul=int(request.POST.get('upper_limit'))
        lt=int(request.POST.get('lower_threshold'))
        # print(lt,type(lt))
        tank_data = {
            "h": h,
            "ul": ul,
            "lt": lt
        }
        enable=bool(request.POST.get('is_active'))
        sth=int(request.POST.get('time_start_h'))
        stm=int(request.POST.get('time_start_m'))
        eth=int(request.POST.get('time_end_h'))
        etm=int(request.POST.get('time_end_m'))
        print(enable,type(enable))        
        time_data = {
            "en": enable,
            "sth": sth,
            "stm": stm,
            "eth": eth,
            "etm": etm        
        }

        # Convert the data to JSON format
        json_tank_data = json.dumps(tank_data)
        json_time_data = json.dumps(time_data)
        publish.single("rpi/broadcast/metrics", json_tank_data, hostname="127.0.0.1", port=1883)
        publish.single("rpi/broadcast/time", json_time_data, hostname="127.0.0.1", port=1883)
                   
        # print(tank_form.is_valid())
        # print(time_profile_form.is_valid())
        print(time_profile_form.errors)
        # print('Checkbox value:', request.POST.get('is_active'))  # Should show "on" if checked, otherwise None

        
        if tank_form.is_valid() and time_profile_form.is_valid():
            tank_form.save()
            time_profile_form.save()
            
        return render(request, 'tank/home.html', {
            'title': 'Home',
            # 'all': all_members
            'tank': tank,
            'time_profile': time_profile
            })
    
    # all_members=Member.objects.all
    return render(request, 'tank/home.html', {
            'title': 'Home',
            # 'all': all_members
            'tank': tank,
            'time_profile': time_profile
        })
    
def logs(request):
    data=SensorData.objects.all
    return render(request, 'tank/logs.html', {
            'title': 'Logs',
            'data': data
        })