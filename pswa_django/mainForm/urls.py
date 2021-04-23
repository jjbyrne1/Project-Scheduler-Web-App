from django.urls import path
from . import views

urlpatterns = [
    path('', views.showtable, name='tableForm'),
    path('table/', views.showtable, name='tableForm'),
    path('info/', views.EditTeamInformation, name='infoForm')
    #path('mainform/forms/MyForm', views.EditTeamInformation, name="infoForm"),
    #path('', views.EditTeamInformation, name='infoForm')
]