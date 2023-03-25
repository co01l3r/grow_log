from django.db.models import Avg
from records.models import Log
from records.forms import LogForm
from django.contrib import messages


def calculate_average_veg_day_temp(cycle):
    veg_logs = Log.objects.filter(cycle=cycle, phase='vegetative')
    veg_day_temp_logs = veg_logs.exclude(temperature_day=None)
    if veg_day_temp_logs.exists():
        avg_day_temp = veg_day_temp_logs.aggregate(Avg('temperature_day'))['temperature_day__avg']
    else:
        avg_day_temp = None
    return avg_day_temp


def fill_and_submit_log_form(cycle, initial_data, request):
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
    log.water = initial_data.get('water')
    log.comment = initial_data.get('comment')

    if request:
        messages.success(request, 'Log created successfully')

    log.save()
