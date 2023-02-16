from django.shortcuts import render, get_object_or_404
from .models import Cycle, Log, Nutrient, NutrientLog
from .utils import calculate_average_veg_temp
from .forms import CycleForm


def records(request):
    cycles = Cycle.objects.all()
    return render(request, 'records/records.html', {'cycles': cycles})


def record(request, pk):
    cycle = get_object_or_404(Cycle, pk=pk)
    logs = Log.objects.filter(cycle=cycle)

    context = {'cycle': cycle, 'logs': logs}
    return render(request, 'records/record.html', context)


def phase_summary(request, pk):
    cycle = Cycle.objects.get(id=pk)
    avg_day_temp = calculate_average_veg_temp(cycle)

    context = {'cycle': cycle, 'avg_day_temp': avg_day_temp}
    return render(request, 'records/record.html', context)
