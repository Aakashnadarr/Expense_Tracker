
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('delete/<uuid:uuid>/', deletetransaction, name='deletetransaction'),
]