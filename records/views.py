from django.shortcuts import render, get_object_or_404
from .models import Cycle, Log, Nutrient, NutrientLog
from .utils import calculate_average_veg_day_temp
from .forms import CycleForm
from django.shortcuts import redirect


# record views
def records(request):
    cycles = Cycle.objects.all()
    return render(request, 'records/records.html', {'cycles': cycles})


def record(request, pk):
    cycle = get_object_or_404(Cycle, id=pk)
    logs = Log.objects.filter(cycle=cycle)

    context = {'cycle': cycle, 'logs': logs}
    return render(request, 'records/record.html', context)


def create_or_edit_record(request, pk=None):
    cycle = get_object_or_404(Cycle, id=pk) if pk else None
    submitted = False  # Flag to indicate if the form has been submitted before

    if request.method == 'POST':
        form = CycleForm(request.POST, instance=cycle)
        if form.is_valid():
            cycle = form.save(commit=False)
            cycle.is_submitted = True  # set is_submitted to True
            cycle.save()
            submitted = True
            return redirect('record', pk=cycle.id)
    else:
        is_editing = True if pk else False  # check if editing a record
        form = CycleForm(instance=cycle, is_editing=is_editing)  # pass is_editing flag to CycleForm

    return render(request, 'records/new_record.html', {'form': form, 'cycle': cycle, 'submitted': submitted})


def delete_record(request, pk):
    cycle = get_object_or_404(Cycle, id=pk)
    cycle.delete()
    return redirect('records')


# log views
# nutrient views
# nutrientLog views
# other views
def phase_summary(request, pk):
    # TODO: tests or delete it
    cycle = Cycle.objects.get(id=pk)
    avg_day_temp = calculate_average_veg_day_temp(cycle)

    context = {'cycle': cycle, 'avg_day_temp': avg_day_temp}
    return render(request, 'records/record.html', context)
