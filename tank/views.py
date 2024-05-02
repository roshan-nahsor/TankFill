from django.shortcuts import render
# from django.http import HttpResponse
from .models import Tank
from .forms import TankForm

# Create your views here.
def tank(request):
    return render(request, 'tank/tank.html', {'title': 'Tank Page'})

def home(request):
    tank=Tank.objects.first()

    if request.method=="POST":
        form=TankForm(request.POST, instance=tank)
        if form.is_valid():
            form.save()
        return render(request, 'tank/home.html', {
            'title': 'Home Page',
            # 'all': all_members
            'tank': tank
            })
    
    # all_members=Member.objects.all
    return render(request, 'tank/home.html', {
        'title': 'Home Page',
        # 'all': all_members
        'tank': tank
        })
    
    
        
    