from django.urls import path
from . import views

urlpatterns = [
    path('', views.showtable, name='tableForm'),
    path('table/', views.showtable, name='tableForm'),
]