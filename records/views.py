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
def create_or_edit_log(request, pk):
    cycle = get_object_or_404(Cycle, pk=pk)
    last_log = cycle.logs.last()

    if request.method == 'POST':
        form = LogForm(request.POST, request.FILES)
        if form.is_valid():
            log = form.save(commit=False)
            log.cycle = cycle
            # update the log instance with the cleaned form data
            log.phase = form.cleaned_data['phase']
            log.temperature_day = form.cleaned_data['temperature_day']
            log.temperature_night = form.cleaned_data['temperature_night']
            log.humidity_day = form.cleaned_data['humidity_day']
            log.humidity_night = form.cleaned_data['humidity_night']
            log.ph = form.cleaned_data['ph']
            log.ec = form.cleaned_data['ec']
            log.irrigation = form.cleaned_data['irrigation']
            log.light_height = form.cleaned_data['light_height']
            log.light_power = form.cleaned_data['light_power']
            log.calibration = form.cleaned_data['calibration']
            log.water = form.cleaned_data['water']
            log.comment = form.cleaned_data['comment']
            log.save()
            messages.success(request, 'Log created successfully')
            return redirect('record', pk=cycle.pk)
        else:
            messages.error(request, 'Log creation failed')
    else:
        initial_data = {}
        if last_log:
            initial_data['phase'] = last_log.phase
            initial_data['temperature_day'] = last_log.temperature_day
            initial_data['temperature_night'] = last_log.temperature_night
            initial_data['humidity_day'] = last_log.humidity_day
            initial_data['humidity_night'] = last_log.humidity_night
            initial_data['ph'] = last_log.ph
            initial_data['ec'] = last_log.ec
            initial_data['irrigation'] = last_log.irrigation
            initial_data['light_height'] = last_log.light_height
            initial_data['light_power'] = last_log.light_power
            initial_data['calibration'] = False
            initial_data['water'] = None
            initial_data['comment'] = ''

            form = LogForm(initial=initial_data)

            # automatically submit the form if last log exist
            log = form.save(commit=False)
            log.cycle = cycle

            # update the log instance with the initial data
            log.phase = initial_data['phase']
            log.temperature_day = initial_data['temperature_day']
            log.temperature_night = initial_data['temperature_night']
            log.humidity_day = initial_data['humidity_day']
            log.humidity_night = initial_data['humidity_night']
            log.ph = initial_data['ph']
            log.ec = initial_data['ec']
            log.irrigation = initial_data['irrigation']
            log.light_height = initial_data['light_height']
            log.light_power = initial_data['light_power']
            log.calibration = initial_data['calibration']
            log.water = initial_data['water']
            log.comment = initial_data['comment']

            log.save()
            messages.success(request, 'Log created successfully')

            return redirect('record', pk=cycle.pk)
        else:
            form = LogForm()

    return render(request, 'records/new_log.html', {'form': form, 'cycle': cycle})
# nutrient views
# nutrientLog views
# other views
def phase_summary(request, pk):
    # TODO: tests or delete it
    cycle = Cycle.objects.get(id=pk)
    avg_day_temp = calculate_average_veg_day_temp(cycle)

    context = {'cycle': cycle, 'avg_day_temp': avg_day_temp}
    return render(request, 'records/record.html', context)
