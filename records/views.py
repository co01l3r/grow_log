from django.shortcuts import render, get_object_or_404
from .models import Cycle, Log, Nutrient, NutrientLog
from .utils import calculate_average_veg_day_temp
from .forms import CycleForm, LogForm
from django.shortcuts import redirect


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
    cycle = get_object_or_404(Cycle, id=pk)
    log = None

    if request.method == 'POST':
        form = LogForm(request.POST, request.FILES)
        if form.is_valid():
            log = form.save(commit=False)
            log.cycle = cycle
            log.save()
    else:
        last_log = Log.objects.filter(cycle=cycle).last()
        initial_data = {}
        if last_log:
            initial_data = {
                'temperature_day': last_log.temperature_day,
                'temperature_night': last_log.temperature_night,
                'humidity_day': last_log.humidity_day,
                'humidity_night': last_log.humidity_night,
                'ph': last_log.ph,
                'ec': last_log.ec,
                'irrigation': last_log.irrigation,
                'light_height': last_log.light_height,
                'light_power': last_log.light_power,
                'calibration': last_log.calibration,
            }
        form = LogForm(initial=initial_data)

    context = {'form': form, 'cycle': cycle, 'log': log}
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
