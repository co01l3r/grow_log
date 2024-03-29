from datetime import date

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpRequest, HttpResponse, HttpResponseNotFound, \
    Http404
from django.db.models import QuerySet

from .models import Cycle, Log, Nutrient, NutrientLog, ReservoirLog
from .forms import CycleForm, LogForm, NutrientLogForm, ReservoirLogForm
from .utils import calculate_average_veg_day_temp, fill_and_submit_log_form


# record views
def records(request: HttpRequest) -> HttpResponse:
    """
    A view that retrieves all Cycle objects from the database and renders them
    in the 'records/records.html' template.

    Parameters:
        request (HttpRequest):
            An HTTP request object that contains metadata about the current
            request.

    Returns:
        HttpResponse:
            A rendered HttpResponse object that contains the rendered
            'records/records.html' template with the retrieved Cycle objects as
            context.
    """
    try:
        cycles = Cycle.objects.all()
    except Cycle.DoesNotExist:
        cycles = []

    context = {'cycles': cycles}
    return render(request, 'records/records.html', context)


def record(request: HttpRequest, pk: str) -> HttpResponse:
    """
    A view that retrieves a single Cycle object from the database based on the
    given primary key (pk), along with any related Log objects, and renders
    them in the 'records/record.html' template.

    Parameters:
        request (HttpRequest):
            An HTTP request object that contains metadata about the current
            request.
        pk (str):
            The string representation of the UUID primary key of the Cycle object
             to retrieve.

    Returns:
        HttpResponse:
            A rendered HttpResponse object that contains the rendered
            'records/record.html' template with the retrieved Cycle and Log
            objects as context. If the Cycle object with the given pk is not
            found in the database, a 404 HTTP response will be returned.
    """
    try:
        cycle = Cycle.objects.get(id=pk)
    except Cycle.DoesNotExist:
        return HttpResponseNotFound("Cycle not found")

    logs = Log.objects.filter(cycle=cycle)
    today = date.today()

    context = {
        'cycle': cycle,
        'logs': logs,
        'today': today
    }
    return render(request, 'records/record.html', context)


def create_or_edit_record(request: HttpRequest, pk: str = None) -> HttpResponse:
    """
    A view that handles the creation or editing of Cycle objects in the database.
    If a primary key (pk) is provided, the function retrieves the Cycle object with
    that primary key from the database and populates the form with its data. If no pk
    is provided, the function assumes that the user wants to create a new Cycle object.

    The function handles both GET and POST requests. On a GET request, the function
    generates an empty CycleForm object and passes it as context to the
    'records/record_form.html' template. On a POST request, the function processes the
    submitted form data and either updates an existing Cycle object or creates a new
    one, depending on whether a pk was provided.

    Parameters:
        request (HttpRequest):
            An HTTP request object that contains metadata about the current
            request.
        pk (str, optional):
            The string representation of the UUID primary key of the Cycle object to edit,
             if editing an existing object. Defaults to None, indicating that a new object
              should be created.

    Returns:
        HttpResponse:
            A rendered HttpResponse object that contains the rendered
            'records/record_form.html' template, along with a CycleForm object
            pre-populated with the data from an existing Cycle object (if pk was
            provided), or an empty CycleForm object (if creating a new object).
            If the form submission is successful, the function redirects the user
            to the 'record' view for the newly created or updated Cycle object.
            If the form submission is not successful, the function re-renders the
            'records/record_form.html' template with an error message.
    """
    try:
        cycle = Cycle.objects.get(id=pk) if pk else None
    except Cycle.DoesNotExist:
        return HttpResponseNotFound("Cycle not found")

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
            messages.error(request, 'An error occurred while creating the cycle')
    else:
        form = CycleForm(instance=cycle)

    context = {
        'form': form,
        'cycle': cycle
    }
    return render(request, 'records/record_form.html', context)


def delete_record(request: HttpRequest, pk: str) -> HttpResponse:
    """
    A view that handles the deletion of a Cycle object from the database.

    The function retrieves the Cycle object with the specified primary key (pk)
    from the database and deletes it. The function then redirects the user to
    the 'records' view.

    Parameters:
        request (HttpRequest):
            An HTTP request object that contains metadata about the current
            request.
        pk (str):
            The string representation of the UUID primary key of the Cycle object to
             delete.

    Returns:
        HttpResponse:
            A redirect HttpResponse object that redirects the user to the 'records'
            view after the specified Cycle object has been deleted.
    """
    try:
        cycle = get_object_or_404(Cycle, id=pk)
        cycle.delete()
        messages.success(request, 'Cycle deleted successfully')
    except Exception as e:
        messages.error(request, f'An error occurred while deleting the cycle: {str(e)}')
    return redirect('records')


# log views
def create_log(request: HttpRequest, pk: str) -> HttpResponse:
    """
    A view that handles the creation of a new Log object for a specified Cycle.

    The function retrieves the Cycle object with the specified primary key (pk)
    from the database and creates a new Log object associated with it. If the
    request method is POST, the function validates the form data and saves the
    new Log object to the database. If the form data is invalid, the function
    returns an HttpResponseBadRequest object. If the request method is not POST,
    the function displays an empty LogForm for the user to fill out.

    Parameters:
        request (HttpRequest):
            An HTTP request object that contains metadata about the current
            request.
        pk (str):
            The string representation of the UUID primary key of the Cycle object
            to which the new Log object is associated.

    Returns:
        HttpResponse:
            A redirect HttpResponse object that redirects the user to the 'record'
            view after the new Log object has been created and saved to the database.
            If the form data is invalid, the function returns an HttpResponseBadRequest
            object. If the request method is not POST, the function returns a rendered
            HTML template that displays an empty LogForm for the user to fill out.
    """
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
            messages.error(request, 'An error occurred while creating the log')
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
                'carbon_dioxide': last_log.carbon_dioxide,
                'comment': '',
            }
            fill_and_submit_log_form(cycle, initial_data, request)
            return redirect('record', pk=cycle.pk)
        else:
            form = LogForm()

            context = {
                'form': form,
                'cycle': cycle
            }
            return render(request, 'records/log_form.html', context)


def edit_log(request: HttpRequest, pk: str, log_pk: int) -> HttpResponse:
    """
    A view for editing an existing log record for a cycle.

    Parameters:
        request (HttpRequest):
            An HttpRequest object that contains metadata about the request.
        pk (str):
            The string representation of the UUID primary key of the Cycle to which the log belongs.
        log_pk (int):
            An integer representing the primary key of the log to edit.

    Returns:
        If the request method is 'POST' and the form is invalid, an error message is returned.
        Otherwise, if the request method is 'POST' and the form is valid, the log record is updated and a redirect
        to the record view is returned. Otherwise, if the request method is 'GET', the edit log form is displayed.
    """
    try:
        cycle = get_object_or_404(Cycle, pk=pk)
        log = get_object_or_404(Log, pk=log_pk, cycle=cycle)
    except Http404:
        return HttpResponseNotFound()

    form = LogForm(request.POST or None, instance=log)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Log updated successfully')
            return redirect('record', pk=pk)
        else:
            messages.error(request, 'An error occurred while updating the log')

    context = {'form': form}
    return render(request, 'records/log_form.html', context)


def delete_log(request: HttpRequest, pk: str, log_pk: int) -> HttpResponse:
    """
    A view that handles the deletion of a Log object from the database.

    The function retrieves the Log object with the specified primary key (log_pk)
    from the database and deletes it. The function then redirects the user to
    the 'record' view for the Cycle object that the deleted Log object belonged to.

    Parameters:
        request (HttpRequest):
            An HTTP request object that contains metadata about the current
            request.
        pk (str):
            The string representation of the UUID primary key of the Cycle object
            that the Log object to be deleted belongs to.
        log_pk (int):
            The primary key of the Log object to delete.

    Returns:
        HttpResponse:
            A redirect HttpResponse object that redirects the user to the 'record'
            view for the Cycle object that the deleted Log object belonged to.
    """
    try:
        log = get_object_or_404(Log, id=log_pk)
        cycle_id = log.cycle.id
        log.delete()
        messages.success(request, 'Log deleted successfully')
    except Exception as e:
        messages.error(request, f'An error occurred while deleting the log: {str(e)}')
    return redirect('record', pk=cycle_id)


# nutrient views
# nutrientLog & reservoirLog views
def create_feeding_log(request: HttpRequest, pk: str, log_pk: int) -> HttpResponse:
    """
    Create a nutrient or reservoir log for a given cycle and log.

    Parameters:
        request (HttpRequest):
            An HttpRequest object that contains metadata about the request.
        pk (str):
            The string representation of the UUID primary key of the Cycle to which the log belongs.
        log_pk (int):
            An integer representing the primary key of the log to edit.

    Returns:
        HttpResponse: The HTTP response that renders the nutrient or reservoir log form.

    Raises:
        Http404: If either the cycle or the log does not exist.
        Exception: If any other error occurs while creating the nutrient or reservoir log.
    """
    try:
        cycle: Cycle = get_object_or_404(Cycle, pk=pk)
        log: Log = get_object_or_404(Log, pk=log_pk, cycle=cycle)
        existing_nutrient_logs: QuerySet[NutrientLog] = log.nutrient_logs.all()
        existing_reservoir_logs: QuerySet[ReservoirLog] = log.reservoir_logs.all()

        if request.method == 'POST':
            nutrient_log_form: NutrientLogForm = NutrientLogForm(request.POST)
            reservoir_log_form: ReservoirLogForm = ReservoirLogForm(request.POST)

            if nutrient_log_form.is_valid():
                nutrient_log: NutrientLog = nutrient_log_form.save(commit=False)
                nutrient_log.log = log
                nutrient_log.save()
                messages.success(request, 'Nutrient log created successfully')
                return HttpResponseRedirect(request.path_info)

            if reservoir_log_form.is_valid():
                reservoir_log: ReservoirLog = reservoir_log_form.save(commit=False)
                reservoir_log.log = log
                reservoir_log.save()
                messages.success(request, 'Reservoir log created successfully.')
                return HttpResponseRedirect(request.path_info)
        else:
            nutrient_log_form: NutrientLogForm = NutrientLogForm()
            reservoir_log_form: ReservoirLogForm = ReservoirLogForm()

        context = {
            'nutrient_log_form': nutrient_log_form,
            'reservoir_log_form': reservoir_log_form,
            'cycle': cycle,
            'existing_nutrient_logs': existing_nutrient_logs,
            'existing_reservoir_logs': existing_reservoir_logs
        }
        return render(request, 'records/feeding_log_form.html', context)

    except (Cycle.DoesNotExist, Log.DoesNotExist):
        messages.error(request, 'Cycle or Log does not exist')
        return HttpResponseRedirect(reverse('/'))
    except Exception as e:
        messages.error(request, f'An error occurred while creating feeding log: {str(e)}')
        return HttpResponseRedirect(request.path_info)


def delete_nutrient_log(request: HttpRequest, pk: str, log_pk: int, nutrient_log_pk: int) -> HttpResponse:
    """
    A view that handles the deletion of a NutrientLog object for a specified Cycle and Log.

    Parameters:
        request (HttpRequest):
            The HTTP request object.
        pk (str):
            The string representation of the UUID primary key of the Cycle to which the log belongs.
        log_pk (int):
            The primary key of the log for which to delete the nutrient log.
        nutrient_log_pk (int):
            The primary key of the nutrient log to delete.

    Returns:
        A redirect HttpResponse object that redirects the user back to form.
    """
    try:
        nutrient_log: NutrientLog = get_object_or_404(NutrientLog, pk=nutrient_log_pk, log__pk=log_pk)
        nutrient_log.delete()
        messages.success(request, 'Nutrient log deleted successfully')
    except Exception as e:
        messages.error(request, f'An error occurred while deleting the nutrient log: {str(e)}')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_reservoir_log(request: HttpRequest, pk: str, log_pk: int, reservoir_log_pk: int) -> HttpResponse:
    """
    A view that handles the deletion of a NutrientLog object for a specified Cycle and Log.

    Parameters:
        request (HttpRequest):
            The HTTP request object.
        pk (str):
            The string representation of the UUID primary key of the Cycle to which the log belongs.
        log_pk (int):
            The primary key of the log for which to delete the nutrient log.
        reservoir_log_pk (int):
            The primary key of the reservoir log to delete.

    Returns:
        A redirect HttpResponse object that redirects the user back to form.
    """
    try:
        reservoir_log: NutrientLog = get_object_or_404(ReservoirLog, pk=reservoir_log_pk, log__pk=log_pk)
        reservoir_log.delete()
        messages.success(request, 'Reservoir log deleted successfully')
    except Exception as e:
        messages.error(request, f'An error occurred while deleting the reservoir log: {str(e)}')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# other views
def phase_summary(request, pk):
    # TODO: tests or delete it
    cycle = Cycle.objects.get(id=pk)
    avg_day_temp = calculate_average_veg_day_temp(cycle)

    context = {'cycle': cycle, 'avg_day_temp': avg_day_temp}
    return render(request, 'records/record.html', context)
