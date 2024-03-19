from django.shortcuts import render, redirect
from services.models import Service
from .forms import ServiceForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index_customer_s(request):
    return render(request, 'services/index_customer_s.html')

@login_required
def services(request):
    if request.user.is_superuser or request.user.is_staff:
        services_list = Service.objects.all()
        return render(request, 'services/index.html', {'services_list': services_list})
    else:
        services_list = Service.objects.all()
        return render(request, 'services/index_customer_s.html', {'services': services_list}) # Redirigir a una página por defecto


def change_status_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    service.status = not service.status
    service.save()
    return redirect('services')  

def create_service(request):
    form = ServiceForm(request.POST or None, request.FILES or None)
    if form.is_valid() and request.method == 'POST':
        try:
            form.save()
            messages.success(request, 'Servicio creado correctamente.')
        except:
            messages.error(request, 'Ocurrió un error al crear el servicio.')        
        return redirect('services')    
    return render(request, 'services/create.html', {'form': form})

def detail_service(request,service_id):
    service = Service.objects.get(pk=service_id)
    data = { 'name': service.name, 'value': service.value}
    return JsonResponse(data)

def delete_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    try:
        service.delete()        
        messages.success(request, 'Servicio eliminado correctamente.')
    except:
        messages.error(request, 'No se puede eliminar el servicio porque está asociado a una reserva.')
    return redirect('services')

def edit_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    form = ServiceForm(request.POST or None, request.FILES or None, instance=service)
    if form.is_valid() and request.method == 'POST':
        try:
            form.save()
            messages.success(request, 'Servicio actualizado correctamente.')
        except:
            messages.error(request, 'Ocurrió un error al editar el servicio.')        
        return redirect('services')    
    return render(request, 'services/editar.html', {'form': form})