from django.db.models import Avg
from records.models import Log


def calculate_average_veg_day_temp(cycle):
    veg_logs = Log.objects.filter(cycle=cycle, phase='vegetative')
    veg_day_temp_logs = veg_logs.exclude(temperature_day=None)
    if veg_day_temp_logs.exists():
        avg_day_temp = veg_day_temp_logs.aggregate(Avg('temperature_day'))['temperature_day__avg']
    else:
        avg_day_temp = None
    return avg_day_temp


def fill_log_without_prompt(cycle, initial_data):
    log = Log.objects.create(
        cycle=cycle,
        phase=initial_data.get('phase'),
        temperature_day=initial_data.get('temperature_day'),
        temperature_night=initial_data.get('temperature_night'),
        humidity_day=initial_data.get('humidity_day'),
        humidity_night=initial_data.get('humidity_night'),
        ph=initial_data.get('ph'),
        ec=initial_data.get('ec'),
        irrigation=initial_data.get('irrigation'),
        light_height=initial_data.get('light_height'),
        light_power=initial_data.get('light_power'),
        calibration=initial_data.get('calibration'),
        water=initial_data.get('water'),
        comment=initial_data.get('comment')
    )
