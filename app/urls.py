
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('delete/<uuid:uuid>/', deletetransaction, name='deletetransaction'),
]