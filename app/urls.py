from django.urls import path

from .views import *

urlpatterns = [
    path('login/', check_login, name='check_login'),
    path('', check_login, name='check_login'),
    path('home', home, name='home'),
    path('new_order', new_order, name='new_order'),
    path('get_active_orders', get_active_orders, name='get_active_orders')

]
