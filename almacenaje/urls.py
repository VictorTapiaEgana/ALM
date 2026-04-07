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
    path('', include('bodega.urls', namespace='bodega')),    

    
]