from django import forms

from .models import Cycle, Log, Nutrient, NutrientLog, ReservoirLog


# record modelForm
class CycleForm(forms.ModelForm):
    """
    A form for creating or updating a Cycle instance.

    Fields:
        light_type(CharField): The type of light fixture used for the growth, a string value up to 32 characters
        fixture (CharField): Fixture model used, a string value up to 80 characters.
        name (CharField): The name given to the cycle, a string value up to 80 characters.
        genetics (CharField): The genetics of the plant being grown, a string value up to 150 characters.
        seedbank (CharField): The seed bank where the seeds were purchased from, a string value up to 80 characters.
        reproductive_cycle (CharField): The type of plant reproductive cycle, either "auto-flowering", "photoperiodic".
        seed_type (CharField): The type of seeds used, either "regular", "feminized", or "clones".
        grow_medium (CharField): The type of grow medium used for the growth, a string value up to 30 characters.
        hydro_system (CharField): The type of hydro system used for the growth, a string value up to 37 characters.

    Methods:
        __init__: Initializes the form with proper attributes and classes for styling.
    """
    class Meta:
        model = Cycle
        exclude = ['id', 'date']
        # fields = ['name', 'genetics', 'light_type', 'fixture', 'reproductive_cycle', 'seed_type', 'seedbank', 'grow_medium']

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super(CycleForm, self).__init__(*args, **kwargs)
        self.fields['reproductive_cycle'].widget.attrs.update({'class': 'form-control'})
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
        self.fields['temperature_day'].widget.attrs.update({'class': 'form-control'})
        self.fields['temperature_night'].widget.attrs.update({'class': 'form-control'})
        self.fields['humidity_day'].widget.attrs.update({'class': 'form-control'})
        self.fields['humidity_night'].widget.attrs.update({'class': 'form-control'})
        self.fields['ph'].widget.attrs.update({'class': 'form-control'})
        self.fields['ec'].widget.attrs.update({'class': 'form-control'})
        self.fields['irrigation'].widget.attrs.update({'class': 'form-control'})
        self.fields['light_height'].widget.attrs.update({'class': 'form-control', 'step': '5.00'})
        self.fields['light_power'].widget.attrs.update({'class': 'form-control'})
        self.fields['calibration'].widget.attrs.update({'class': 'form-check-input'})


# nutrient modelForm
# nutrientLog modelForm
class NutrientLogForm(forms.ModelForm):
    """
    A form for creating a NutrientLog instance.

    Fields:
        nutrient (ForeignKey): A foreign key referencing the `Nutrient` model this nutrient log corresponds to.
        concentration (IntegerField): An integer representing the concentration of the nutrient for this log.

    Methods:
        __init__: Initializes the form with proper attributes and classes for styling.
    """
    class Meta:
        model = NutrientLog
        fields = ['nutrient', 'concentration']

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.fields['nutrient'].widget.attrs.update({'class': 'form-control'})
        self.fields['concentration'].widget.attrs.update({'class': 'form-control'})


# ReservoirLog modelForm
class ReservoirLogForm(forms.ModelForm):
    """
    A form for creating a ReservoirLog instance.

    Fields:
        reverse_osmosis (CharField): A character field representing whether reverse osmosis is used or not.
        water (IntegerField): An optional integer field representing the amount of water.
        waste_water (IntegerField): An optional integer field representing the amount of waste water.

    Methods:
        __init__: Initializes the form with proper attributes and classes for styling.
    """

    class Meta:
        model = ReservoirLog
        fields = ['reverse_osmosis', 'water', 'waste_water']

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.fields['reverse_osmosis'].widget.attrs.update({'class': 'form-control'})
        self.fields['water'].widget.attrs.update({'class': 'form-control'})
        self.fields['waste_water'].widget.attrs.update({'class': 'form-control'})
