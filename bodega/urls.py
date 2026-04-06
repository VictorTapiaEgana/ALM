from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.registro_usuario, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
