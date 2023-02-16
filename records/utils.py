from django.db.models import Avg
from records.models import Log


def calculate_average_veg_temp(cycle):
    veg_logs = Log.objects.filter(cycle=cycle, phase='vegetative')
    veg_day_temp_logs = veg_logs.exclude(temperature_day=None)
    if veg_day_temp_logs.exists():
        avg_day_temp = veg_day_temp_logs.aggregate(Avg('temperature_day'))['temperature_day__avg']
    else:
        avg_day_temp = None
    return avg_day_temp
