def recover_password(request):    
    if request.method == 'POST':
        email = request.POST.get('email', '')  # Obtener el email del formulario
        
        # Verificar si el email existe en la base de datos
        if User.objects.filter(email=email).exists():
            """ Cosultar el usuario por el correo  y cambiar la contraseña encriptada"""
            recuperar_contraseña(email)
            return redirect('login')
        else:
            messages.error(request, 'Inserte un correo existente.')
            return render(request, 'restore.html')
    
    return render(request, 'restore.html')


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string

from django.shortcuts import render

def generar_contraseña():
    caracteres = string.ascii_letters + string.digits
    longitud = 10
    return ''.join(random.choice(caracteres) for i in range(longitud))

def enviar_correo(destinatario, contraseña):
    # Configuración del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    puerto = 587
    remitente = 'glampingcelestial@gmail.com'
    contraseña_smtp = 'uoob mcva wojt adal'

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = 'Recuperación de contraseña'

    cuerpo = f'Tu nueva contraseña es: {contraseña}'
    mensaje.attach(MIMEText(cuerpo, 'plain' , 'utf-8'))

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
    if cambiar_contraseña_usuario(correo_destino, nueva_contraseña):
        print("La contraseña del usuario ha sido cambiada exitosamente.")
    else:
        print("No se pudo cambiar la contraseña del usuario. El usuario no fue encontrado.")

from django.contrib.auth.models import User

def cambiar_contraseña_usuario(email, nueva_contraseña):
    try:
        usuario = User.objects.get(email=email)
        usuario.set_password(nueva_contraseña)
        usuario.save()
        return True  # Indica que la contraseña fue cambiada exitosamente
    except User.DoesNotExist:
        return False  # Indica que no se encontró ningún usuario con el correo electrónico especificado