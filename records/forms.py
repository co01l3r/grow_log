from django import forms

from .models import Cycle, Log, Nutrient, NutrientLog


# record modelForm
class CycleForm(forms.ModelForm):
    """
    A form for creating or updating a Cycle instance.

    Fields:
        name (CharField): The name of the cycle.
        genetics (CharField): The genetics of the cycle.
        seedbank (CharField): The seedbank of the cycle.
        fixture (CharField): The fixture used for the cycle.
        behavioral_response (ChoiceField): The behavioral response of the cycle.
        seed_type (ChoiceField): The type of seed used for the cycle.
        grow_medium (ChoiceField): The grow medium used for the cycle.

    Methods:
        __init__: Initializes the form with proper attributes and classes for styling.
    """
    class Meta:
        model = Cycle
        fields = ['name', 'genetics', 'seedbank', 'fixture', 'behavioral_response', 'seed_type', 'grow_medium']

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super(CycleForm, self).__init__(*args, **kwargs)
        self.fields['behavioral_response'].widget.attrs.update({'class': 'form-control'})
        self.fields['seed_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['grow_medium'].widget.attrs.update({'class': 'form-control'})


# log modelForm
class LogForm(forms.ModelForm):
    """
    A form for creating or updating a Log instance.

    Fields:
        temperature_day (DecimalField): The temperature during the day.
        temperature_night (DecimalField): The temperature during the night.
        humidity_day (DecimalField): The humidity during the day.
        humidity_night (DecimalField): The humidity during the night.
        ph (DecimalField): The pH level of the environment.
        ec (DecimalField): The electrical conductivity of the environment.
        irrigation (CharField): The type of irrigation used.
        light_height (DecimalField): The height of the light source.
        light_power (CharField): The power of the light source.
        calibration (BooleanField): Indicates whether the instrument was calibrated.

    Methods:
        __init__: Initializes the form with proper attributes and classes for styling.
    """
    class Meta:
        model = Log
        exclude = ['cycle', 'date']

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.fields['temperature_day'].widget.attrs.update({'class': 'form-control', 'step': '1.00'})
        self.fields['temperature_night'].widget.attrs.update({'class': 'form-control', 'step': '1.00'})
        self.fields['humidity_day'].widget.attrs.update({'class': 'form-control'})
        self.fields['humidity_night'].widget.attrs.update({'class': 'form-control'})
        self.fields['ph'].widget.attrs.update({'class': 'form-control', 'step': '0.10'})
        self.fields['ec'].widget.attrs.update({'class': 'form-control', 'step': '0.10'})
        self.fields['irrigation'].widget.attrs.update({'class': 'form-control'})
        self.fields['light_height'].widget.attrs.update({'class': 'form-control', 'step': '5.00'})
        self.fields['light_power'].widget.attrs.update({'class': 'form-control'})
        self.fields['calibration'].widget.attrs.update({'class': 'form-check-input'})

# nutrient modelForm
# nutrientLog modelForm
