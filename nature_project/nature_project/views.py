import json
from pyexpat.errors import messages
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from cabins.models import Cabin
from bookings.models import Booking
from services.models import Service
from customers.models import Customer
from payments.models import Payment
from django.db.models import Sum
import calendar
from django.db.models.functions import ExtractMonth
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


def bienvenido(request):
    return render(request, 'bienvenido.html')


def index(request):
    customer_name = request.user.get_username() 

    ingresos_por_mes = Payment.objects.filter(status=True).annotate(
    mes=ExtractMonth('date')
    ).values('mes').annotate(total_ingresos=Sum('value'))
    meses = range(1, 13)

    # Agregar cada mes y su valor a la lista de datos
    data = [["Mes", "Ingresos"]]
    for mes in meses:
        total_mes = 0
        nombre_mes = calendar.month_name[mes]
        for ingreso_mes in ingresos_por_mes:
            if ingreso_mes['mes'] == mes:
                total_mes = ingreso_mes['total_ingresos']
                break
        data.append([nombre_mes, total_mes])


    # --- Fin grafica dashboard ---
    total_pagos = Payment.objects.aggregate(total=Sum('value'))
    count = Cabin.objects.count()
    customer = Customer.objects.count()
    count_booking = Booking.objects.filter(status="Reservado").count()
    count_booking2 = Booking.objects.filter(status="En ejecución").count()
    count_booking3 = Booking.objects.filter(status="Cancelado").count()
    count_booking4 = Booking.objects.filter(status="Confirmado").count()
    total_bookings = count_booking + count_booking2 + count_booking3 + count_booking4;
    total_reservas = count_booking + count_booking2

    
    return render(request, 'index.html', {
        "count": count,
        "count_booking": count_booking,
        "count_booking2": count_booking2,
        "count_booking3": count_booking3,
        "count_booking4": count_booking4,
        "total_reservas": total_reservas,
        "customer": customer,
        'total_pagos': total_pagos['total'],
        "total_bookings": total_bookings,
        'data': json.dumps(data),
        'customer_name': customer_name,
    })


def login(request):
    error = None
    if request.method == 'POST':
        
        ingresos_por_mes = Payment.objects.filter(status=True).annotate(
        mes=ExtractMonth('date')
        ).values('mes').annotate(total_ingresos=Sum('value'))
        meses = range(1, 13)

        # Agregar cada mes y su valor a la lista de datos
        data = [["Mes", "Ingresos"]]
        for mes in meses:
            total_mes = 0
            nombre_mes = calendar.month_name[mes]
            for ingreso_mes in ingresos_por_mes:
                if ingreso_mes['mes'] == mes:
                    total_mes = ingreso_mes['total_ingresos']
                    break
            data.append([nombre_mes, total_mes])


        # --- Fin grafica dashboard ---
        total_pagos = Payment.objects.aggregate(total=Sum('value'))
        count = Cabin.objects.count()
        customer = Customer.objects.count()
        count_booking = Booking.objects.filter(status="Reservado").count()
        count_booking2 = Booking.objects.filter(status="En ejecución").count()
        count_booking3 = Booking.objects.filter(status="Cancelado").count()
        count_booking4 = Booking.objects.filter(status="Confirmado").count()
        total_bookings = count_booking + count_booking2 + count_booking3 + count_booking4;
        total_reservas = count_booking + count_booking2



        username = request.POST['username']
        password = request.POST['password']

        authenticated_user = authenticate(username=username, password=password)
        if request.user.is_superuser or request.user.is_staff:
            auth_login(request, authenticated_user)
<<<<<<< HEAD
            return render(request, 'index.html', {'user': authenticated_user, "count": count,
        "count_booking": count_booking,
        "count_booking2": count_booking2,
        "count_booking3": count_booking3,
        "count_booking4": count_booking4,
        "total_reservas": total_reservas,
        "customer": customer,
        'total_pagos': total_pagos['total'],
        "total_bookings": total_bookings,
        'data': json.dumps(data),})
        
        else: 
            auth_login(request, authenticated_user)
            return render(request, 'cabins/index_customer.html', {'user': authenticated_user})
=======
            return render(request, 'bienvenido.html', {'user': authenticated_user})
        
        else: 
            if authenticated_user is not None:
                auth_login(request, authenticated_user)
                return render(request, 'bienvenido.html', {'user': authenticated_user})
>>>>>>> ca1f4879f7b29381dbbe1a8fec8abbfdca00542b
        
        
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)    
    return redirect('landing')

def landing(request):
    # Obtenemos la sesión del usuario
    # Obtenemos todas las cabañas y servicios
    cabins = Cabin.objects.filter(status=True) 
    services = Service.objects.filter(status=True)

    # Renderizamos la plantilla con ambos conjuntos de datos
    return render(
        request,
        "landing.html",
        {
            "cabins": cabins,
            "services": services,
        },
    )


from nature_project.forms import RegisterForm
from customers.models import Customer
from django.contrib.auth.models import Group

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            document = form.cleaned_data['document']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            username = email
            user = User.objects.create_user(username, email, password, first_name=name, last_name=last_name)
            user.save()
            group = Group.objects.get(name='clientes')
            user.groups.add(group)
            if user is not None:            
                client = Customer.objects.filter(document=document).first()
                if client is None:
                    name = form.cleaned_data['name'] + ' ' + form.cleaned_data['last_name']
                    client = Customer(None, name, document=document, email=email, phone=phone)
                    client.save()
                    return redirect('login')               
            return redirect('login')    
    return render(request, 'register.html', {'form': form})

def recover_password(request):
    mensaje_enviado = False
    
    if request.method == 'POST':
        email = request.POST.get('email', '')  # Obtener el email del formulario
        
        # Verificar si el email existe en la base de datos
        if User.objects.filter(email=email).exists():
            nueva_contraseña = generar_contraseña()  # Generar nueva contraseña
            enviar_correo(email, nueva_contraseña)  # Enviar la nueva contraseña por correo
            
            # Cambiar la contraseña en el usuario correspondiente
            if cambiar_contraseña_usuario(email, nueva_contraseña):
                # Actualizar la sesión del usuario si está autenticado
                if request.user.is_authenticated:
                    update_session_auth_hash(request, request.user)
                
                mensaje_enviado = True  # Marcar como verdadero si el mensaje se envió correctamente
    
    if mensaje_enviado:
        messages.success(request, 'Correo enviado.')
    
    return render(request, 'recover_password.html')

def generar_contraseña():
    caracteres = string.ascii_letters + string.digits
    longitud = 10
    return ''.join(random.choice(caracteres) for i in range(longitud))

def enviar_correo(destinatario, contraseña):
    # Configuración del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    puerto = 587
    remitente = 'naturevip99@gmail.com'
    contraseña_smtp = 'pgre vwvu ahbs zzdq'

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = 'Recuperación de contraseña'

    cuerpo = f'Tu nueva contraseña es: {contraseña}'
    mensaje.attach(MIMEText(cuerpo, 'plain', 'utf-8'))

    # Iniciar sesión en el servidor SMTP
    servidor = smtplib.SMTP(smtp_server, puerto)
    servidor.starttls()
    servidor.login(remitente, contraseña_smtp)

    # Enviar el correo electrónico
    servidor.send_message(mensaje)

    # Cerrar la conexión
    servidor.quit()

# Función principal
def recuperar_contraseña(email):
    correo_destino = email
    nueva_contraseña = generar_contraseña()
    enviar_correo(correo_destino, nueva_contraseña)

from django.contrib.auth.models import User


def cambiar_contraseña_usuario(email, nueva_contraseña):
    try:
        usuario = User.objects.get(email=email)
        usuario.set_password(nueva_contraseña)
        usuario.save()
        return True  # Indica que la contraseña fue cambiada exitosamente
    except User.DoesNotExist:
        return False  # Indica que no se encontró ningún usuario con el correo electrónico especificado
    
    