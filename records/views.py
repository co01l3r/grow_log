from django.shortcuts import render, redirect, get_object_or_404
from .models import Cycle, Log, Nutrient, NutrientLog
from .utils import calculate_average_veg_day_temp, fill_and_submit_log_form
from .forms import CycleForm, LogForm
from django.contrib import messages
from django.http import HttpResponseBadRequest


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
            if pk:
                messages.success(request, 'Record updated successfully')
            else:
                messages.success(request, 'Record created successfully')
            return redirect('record', pk=cycle.id)
        else:
            messages.error(request, 'Record creation failed')
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
            return HttpResponseBadRequest("Log creation failed")
    else:
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
            fill_and_submit_log_form(cycle, initial_data, request)
            return redirect('record', pk=cycle.pk)
        else:
            form = LogForm()
            context = {'form': form, 'cycle': cycle}
            return render(request, 'records/new_log.html', context)


def edit_log(request, pk, log_pk):
    cycle = get_object_or_404(Cycle, pk=pk)
    log = get_object_or_404(Log, pk=log_pk, cycle=cycle)
    form = LogForm(request.POST or None, instance=log)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('record', pk=pk)

    context = {'form': form}
    return render(request, 'records/new_log.html', context)

# nutrient views
# nutrientLog views
# other views
def phase_summary(request, pk):
    # TODO: tests or delete it
    cycle = Cycle.objects.get(id=pk)
    avg_day_temp = calculate_average_veg_day_temp(cycle)

    context = {'cycle': cycle, 'avg_day_temp': avg_day_temp}
    return render(request, 'records/record.html', context)
