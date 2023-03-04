from django.shortcuts import render, get_object_or_404
from .models import Cycle, Log, Nutrient, NutrientLog
from .utils import calculate_average_veg_day_temp
from .forms import CycleForm
from django.shortcuts import redirect


def records(request):
    cycles = Cycle.objects.all()
    return render(request, 'records/records.html', {'cycles': cycles})


def record(request, pk):
    cycle = get_object_or_404(Cycle, pk=pk)
    logs = Log.objects.filter(cycle=cycle)

    context = {'cycle': cycle, 'logs': logs}
    return render(request, 'records/record.html', context)


def create_or_edit_record(request, pk=None):
    # TODO: tests
    if pk:
        cycle = get_object_or_404(Cycle, pk=pk)
    else:
        cycle = None

    if request.method == 'POST':
        form = CycleForm(request.POST, instance=cycle)
        if form.is_valid():
            cycle = form.save()
            return redirect('record', pk=cycle.pk)
    else:
        form = CycleForm(instance=cycle)

    context = {'form': form, 'cycle': cycle}
    return render(request, 'records/new_record.html', context)


def delete_record(request, pk):
    # TODO: tests
    cycle = get_object_or_404(Cycle, pk=pk)
    cycle.delete()
    return redirect('records')


def phase_summary(request, pk):
    # TODO: tests or delete it
    cycle = Cycle.objects.get(id=pk)
    avg_day_temp = calculate_average_veg_day_temp(cycle)

    context = {'cycle': cycle, 'avg_day_temp': avg_day_temp}
    return render(request, 'records/record.html', context)
