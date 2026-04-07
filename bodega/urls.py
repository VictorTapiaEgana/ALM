from django.urls import path
from .views import views, auth_views, productos_views

app_name = 'bodega'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', auth_views.registro_usuario, name='register'),
    path('productos/crear-producto/', productos_views.crear_producto, name='crear_producto'),
    

]
