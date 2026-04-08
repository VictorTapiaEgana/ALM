from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, authenticate, login

from bodega.models import Perfil
User = get_user_model()

# Create your views here.

def login_usuario(request):
    if request.method == 'POST':
    
        correo = request.POST.get('email_usuario')
        clave = request.POST.get('password_usuario')
    
        user = authenticate(request, username=correo, password=clave)

        if user is not None:
            login(request, user)
            return redirect('bodega:dashboard')
        else:
            messages.error(request, "Credenciales incorrectas")

            
    return render(request, 'login.html')

def registro_usuario(request):

    if request.method == 'GET':        
        return render(request, 'login/register.html')

    if request.method == 'POST':

        print(request.POST)
        
        try:
            usuario = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            password_confirm = request.POST.get('password_confirm')

            if not usuario or not password or not password_confirm:
                messages.error(request, 'Usuario, contraseña y confirmación de contraseña son obligatorios')
                return redirect('bodega:register')

            if password != password_confirm:
                messages.error(request, 'Las contraseñas no coinciden')
                return redirect('bodega:register')

            nuevo_usuario = User.objects.create_user(email=email, password=password,username=usuario)            
            perfil = Perfil.objects.create(usuario=nuevo_usuario)

            # messages.success(request, 'Registro exitoso')
            return redirect('bodega:dashboard')            

        except IntegrityError as e:
            messages.error(request, 'Este correo electrónico ya está registrado.')
            return redirect('bodega:register')

        except Exception as e:

            messages.error(request,f'Ocurrió un error inesperado: {str(e)}')
            return redirect('bodega:register')
        


