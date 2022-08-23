from django.urls import path

from .views import *

urlpatterns = [
    path('', check_login, name='check_login'),
    path('login/', check_login, name='check_login'),
    path('home/', home, name='home'),
    path('sign_up/', sign_up, name='sign_up'),
    path('new_order/', new_order, name='new_order'),
    path('get_active_orders/', get_active_orders, name='get_active_orders')

]
