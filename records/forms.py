from django.forms import ModelForm
from .models import Cycle, Log, Nutrient, NutrientLog
from django import forms


class CycleForm(forms.ModelForm):
    class Meta:
        model = Cycle
        fields = ['name', 'genetics', 'seedbank', 'fixture', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }