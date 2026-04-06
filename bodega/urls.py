from django.urls import path
from .views import views, auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', auth_views.registro_usuario, name='register'),
    

]
