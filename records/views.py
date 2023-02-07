from django.shortcuts import render, get_object_or_404
from .models import Cycle, Log, Nutrient, NutrientLog
from .forms import CycleForm


def records(request):
    cycles = Cycle.objects.all()
    return render(request, 'records/records.html', {'cycles': cycles})


def record(request, pk):
    cycle = get_object_or_404(Cycle, pk=pk)
    logs = Log.objects.filter(cycle=cycle)

    context = {'cycle': cycle, 'logs': logs}
    return render(request, 'records/record.html', context)
