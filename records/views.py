from django.shortcuts import render, get_object_or_404
from .models import Cycle, Log, Nutrient, NutrientLog
from .utils import calculate_average_veg_day_temp
from .forms import CycleForm, LogForm
from django.shortcuts import redirect
from django.contrib import messages


# record views
def records(request):
    cycles = Cycle.objects.all()

    context = {'cycles': cycles}
    return render(request, 'records/records.html', context)


def record(request, pk):
    cycle = get_object_or_404(Cycle, id=pk)
    logs = Log.objects.filter(cycle=cycle)

    context = {'cycle': cycle, 'logs': logs}
    return render(request, 'records/record.html', context)


def create_or_edit_record(request, pk=None):
    cycle = get_object_or_404(Cycle, id=pk) if pk else None

    if request.method == 'POST':
        form = CycleForm(request.POST, instance=cycle)
        if form.is_valid():
            cycle = form.save(commit=False)
            cycle.save()
            return redirect('record', pk=cycle.id)
    else:
        is_editing = True if pk else False
        form = CycleForm(instance=cycle, is_editing=is_editing)

    context = {'form': form, 'cycle': cycle}
    return render(request, 'records/new_record.html', context)


def delete_record(request, pk):
    cycle = get_object_or_404(Cycle, id=pk)
    cycle.delete()
    return redirect('records')


# log views
def create_log(request, pk):
    cycle = get_object_or_404(Cycle, pk=pk)
    last_log = cycle.logs.last()

    if request.method == 'POST':
        form = LogForm(request.POST, request.FILES)
        if form.is_valid():
            log = form.save(commit=False)
            log.cycle = cycle
            log.save()
            messages.success(request, 'Log created successfully')
            return redirect('record', pk=cycle.pk)
        else:
            messages.error(request, 'Log creation failed')
    else:
        initial_data = {}
        if last_log:
            initial_data = {
                'phase': last_log.phase,
                'temperature_day': last_log.temperature_day,
                'temperature_night': last_log.temperature_night,
                'humidity_day': last_log.humidity_day,
                'humidity_night': last_log.humidity_night,
                'ph': last_log.ph,
                'ec': last_log.ec,
                'irrigation': last_log.irrigation,
                'light_height': last_log.light_height,
                'light_power': last_log.light_power,
                'calibration': False,
                'water': None,
                'comment': '',
            }

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

        log.save()
        messages.success(request, 'Log created successfully')

        return redirect('record', pk=cycle.pk)

    return render(request, 'records/new_log.html', {'form': form, 'cycle': cycle})


def edit_log(request, pk):
    pass
# nutrient views
# nutrientLog views
# other views
def phase_summary(request, pk):
    # TODO: tests or delete it
    cycle = Cycle.objects.get(id=pk)
    avg_day_temp = calculate_average_veg_day_temp(cycle)

    context = {'cycle': cycle, 'avg_day_temp': avg_day_temp}
    return render(request, 'records/record.html', context)
