from django import forms
from .models import Tank

class TankForm(forms.ModelForm):
    class Meta:
        model=Tank
        fields=['height', 'upper_limit', 'lower_threshold']