from django import forms
from .models import Tank, TimeProfile

class TankForm(forms.ModelForm):
    class Meta:
        model=Tank
        fields=['height', 'upper_limit', 'lower_threshold']
        
class TimeForm(forms.ModelForm):
    class Meta:
        model=TimeProfile
        fields=['is_active', 'time_start_h', 'time_start_m', 'time_end_h', 'time_end_m']