from django.urls import path, include
from . import views

urlpatterns = [
    path('', view=views.home, name='home'),
    path('telemetry_list', view=views.telemetry_list, name='telemetry_list'),
    path('car_list', view=views.car_list, name='car_list'),
    path('user_list', view=views.user_list, name='user_list'),
    path('rental_list', view=views.rental_list, name='rental_list'),
    path('create_telemetry/<int:number>/', view=views.create_telemetry,
         name='create_telemetry'),
    path('create_car/<int:number>/', view=views.create_car, name='create_car'),
    path('create_user/<int:number>/', view=views.create_user, name='create_user'),
    path('create_rental/<int:number>/',
         view=views.create_rental, name='create_rental'),
]
