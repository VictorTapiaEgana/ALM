"""
URL configuration for almacenaje project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # URLs del administrador
    path('admin/', admin.site.urls),       
    # URLs de autenticación
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),        
    # path('register/', auth_views.LoginView.as_view(template_name='login/register.html'), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # URLs de la aplicación
    path('', include('bodega.urls')),    

    
]