from typing import Dict, Optional

from django.http import HttpRequest
from django.contrib import messages
from django.db.models import Avg

from .models import Log
from .forms import LogForm


def calculate_average_veg_day_temp(cycle):
    veg_logs = Log.objects.filter(cycle=cycle, phase='vegetative')
    veg_day_temp_logs = veg_logs.exclude(temperature_day=None)
    if veg_day_temp_logs.exists():
        avg_day_temp = veg_day_temp_logs.aggregate(Avg('temperature_day'))['temperature_day__avg']
    else:
        avg_day_temp = None
    return avg_day_temp


def fill_and_submit_log_form(cycle: 'models.Cycle', initial_data: Dict[str, str], request: Optional[HttpRequest] = None) -> None:
    """
    A function to fill and submit the log form for a given cycle.

    Parameters:
        cycle (Cycle): A Cycle object representing the current growth cycle.
        initial_data (dict): A dictionary of initial data for the log form to be filled with.
        request (HttpRequest, optional): An optional HttpRequest object for displaying messages. Defaults to None.

    Returns:
        None
    """
    form = LogForm(initial=initial_data)
    log = form.save(commit=False)
    log.cycle = cycle

    log.phase = initial_data.get('phase')
    log.temperature_day = initial_data.get('temperature_day')
    log.temperature_night = initial_data.get('temperature_night')
    log.humidity_day = initial_data.get('humidity_day')
    log.humidity_night = initial_data.get('humidity_night')
    log.ph = initial_data.get('ph')
    log.ec = initial_data.get('ec')
    log.irrigation = initial_data.get('irrigation')
    log.light_height = initial_data.get('light_height')
    log.light_power = initial_data.get('light_power')
    log.calibration = initial_data.get('calibration')
    log.carbon_dioxide = initial_data.get('carbon_dioxide')
    log.comment = initial_data.get('comment')

    if request:
        messages.success(request, 'Log created successfully')

    log.save()
