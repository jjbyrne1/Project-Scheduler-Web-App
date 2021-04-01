from django.urls import path
from .views import showtable, my_form, my_form2

urlpatterns = [
    path('', showtable, name='form1'),
    path('', my_form, name='form'),
    path('', my_form2, name='form1')
]