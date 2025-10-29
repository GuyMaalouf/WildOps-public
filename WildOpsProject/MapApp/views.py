# MapApp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Operation  # Import your Operation model
from .forms import OperationForm  # Assuming you have a form for Operation
from shared.constants import PILOT_CHOICES  # Import PILOT_CHOICES
import json

# Create your views here.

def index(request):
    return render(request, 'MapApp/index.html')

@permission_required('MapApp.view_olpejeta', raise_exception=True)
def olpejeta(request):
    return render(request, 'MapApp/olpejeta.html')

@permission_required('MapApp.view_flightcylinders', raise_exception=True)
def flight_cylinders(request):
    latitude = ''
    longitude = ''
    radius = ''
    if request.method == 'POST':
        latitude = request.POST.get('latitude', '')
        longitude = request.POST.get('longitude', '')
        radius = request.POST.get('radius', '')
        # Process the form data as needed
    return render(request, 'MapApp/flight_cylinders.html', {
        'latitude': latitude,
        'longitude': longitude,
        'radius': radius
    })

@permission_required('MapApp.view_utm', raise_exception=True)
def utm_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            operation_id = data.get('operation_id')
            request_state = data.get('request_state')
            if operation_id and request_state:
                operation = get_object_or_404(Operation, operation_id=operation_id)
                operation.request_state = request_state
                operation.save()
                return JsonResponse({'success': True})
        except json.JSONDecodeError:
            operation_id = request.POST.get('operation_id')
            if operation_id:
                operation = get_object_or_404(Operation, operation_id=operation_id)
                form = OperationForm(request.POST, instance=operation, user=request.user)
            else:
                form = OperationForm(request.POST, user=request.user)
            
            if form.is_valid():
                print("Form is valid"),
                operation = form.save(commit=False)
                operation.username = request.user.username  # Ensure the username is set
                operation.request_state = 'requested'
                operation.activation_state = update_activation_state(operation.start_datetime, operation.end_datetime)
                operation.save()
                return redirect('utm')
            else:
                print("Form is invalid")
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        operation_id = data.get('operation_id')
        operation = get_object_or_404(Operation, operation_id=operation_id)
        operation.delete()
        return JsonResponse({'success': True})
    else:
        form = OperationForm(user=request.user)
    
    operations = Operation.objects.all()
    return render(request, 'MapApp/utm.html', {'operations': operations, 'form': form, 'pilot_choices': PILOT_CHOICES})  # Pass PILOT_CHOICES to the template

def update_activation_state(start_datetime, end_datetime):
    now = timezone.now()
    print(f"Current time: {now}, Start time: {start_datetime}, End time: {end_datetime}")
    if now < start_datetime:
        return 'inactive'
    elif start_datetime <= now <= end_datetime:
        return 'active'
    else:
        return 'expired'
    
def utm_map_view(request):
    operations = list(Operation.objects.values())
    return JsonResponse({'operations': operations})

def overview_map_view(request):
    operations = Operation.objects.filter(request_state='approved', activation_state__in=['inactive','active'])
    return render(request, 'MapApp/overview.html', {'operations': operations})

@permission_required('MapApp.view_operationrequest', raise_exception=True)
def operation_request(request):
    if request.method == 'POST':
        operation_id = request.POST.get('operation_id')
        if operation_id:
            operation = get_object_or_404(Operation, pk=operation_id)
            form = OperationForm(request.POST, instance=operation, user=request.user)
        else:
            form = OperationForm(request.POST, user=request.user)

        if form.is_valid():
            print("Form is valid"),
            operation = form.save(commit=False)
            operation.username = request.user.username  # Ensure the username is set
            operation.request_state = 'requested'
            operation.activation_state = update_activation_state(operation.start_datetime, operation.end_datetime)
            operation.save()
            return redirect('operation_request')
        else:
            print("Form is invalid")
            print(form.data)
            print(form.errors)
    else:
        form = OperationForm(user=request.user)
    
    operations = Operation.objects.all()
    return render(request, 'MapApp/operation_request.html', {'operations': operations, 'form': form})