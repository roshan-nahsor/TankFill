from django.shortcuts import render
# from django.http import HttpResponse
from .models import Tank, SensorData
from .forms import TankForm

import paho.mqtt.publish as publish
import json

# Create your views here.
def tank(request):
    return render(request, 'tank/tank.html', {'title': 'Tank Page'})

def home(request):
    tank=Tank.objects.first()
    if request.method=="POST":
        form=TankForm(request.POST, instance=tank)
        h=int(request.POST.get('height'))
        ul=int(request.POST.get('upper_limit'))
        lt=int(request.POST.get('lower_threshold'))
        print(lt,type(lt))
        data = {
            "h": h,
            "ul": ul,
            "lt": lt
        }

        # Convert the data to JSON format
        json_data = json.dumps(data)
        publish.single("rpi/broadcast", json_data, hostname="127.0.0.1", port=1883)
                   
        if form.is_valid():
            form.save()
        return render(request, 'tank/home.html', {
            'title': 'Home',
            # 'all': all_members
            'tank': tank
            })
    
    # all_members=Member.objects.all
    return render(request, 'tank/home.html', {
        'title': 'Home',
        # 'all': all_members
        'tank': tank
        })
    
def logs(request):
    data=SensorData.objects.all
    return render(request, 'tank/logs.html', {
        'title': 'Logs',
         'data': data
        })