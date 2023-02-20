from django.forms import ModelForm
from .models import Cycle, Log, Nutrient, NutrientLog
from django import forms


class CycleForm(forms.ModelForm):
    class Meta:
        model = Cycle
        fields = '__all__'
