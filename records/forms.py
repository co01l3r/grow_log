from django.forms import ModelForm
from .models import Cycle, Log, Nutrient, NutrientLog
from django import forms


class CycleForm(forms.ModelForm):
    class Meta:
        model = Cycle
        fields = ['name', 'genetics', 'seedbank', 'fixture', 'behavioral_response', 'seed_type', 'grow_medium', 'beginning_phase']

    def __init__(self, *args, **kwargs):
        is_editing = kwargs.pop('is_editing', False)
        super(CycleForm, self).__init__(*args, **kwargs)
        self.fields['behavioral_response'].widget.attrs.update({'class': 'form-control'})
        self.fields['seed_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['grow_medium'].widget.attrs.update({'class': 'form-control'})
        if is_editing:
            # if editing, remove beginning_phase field from the form
            self.fields.pop('beginning_phase')
        else:
            self.fields['beginning_phase'].widget.attrs.update({'class': 'form-control'})