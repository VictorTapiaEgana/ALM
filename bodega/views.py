from sqlite3 import IntegrityError
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from bodega.models import Perfil

# Create your views here.
def registro_usuario(request):

    if request.method == 'GET':        
        return render(request, 'login/register.html')

    if request.method == 'POST':

        print(request.POST)
        
        try:
            usuario = request.POST.get('username')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')

            if not usuario or not password or not password_confirm:
                messages.error(request, 'Usuario, contraseña y confirmación de contraseña son obligatorios')
                return redirect('register')

            if password != password_confirm:
                messages.error(request, 'Las contraseñas no coinciden')
                return redirect('register')

            nuevo_usuario = User.objects.create_user(username=usuario, password=password)            
            perfil = Perfil.objects.create(usuario=nuevo_usuario)

            messages.success(request, 'Registro exitoso')
            return redirect('dashboard')            

        except IntegrityError as e:
            messages.error(request, 'El usuario ya existe')
            return redirect('register')

        except Exception as e:

            messages.error(request,f'Ocurrió un error inesperado: {str(e)}')
            return redirect('register')
        

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')
