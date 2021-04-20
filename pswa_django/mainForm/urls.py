from django.urls import path
from .views import showtable

urlpatterns = [
    path('', showtable, name='form1'),
]