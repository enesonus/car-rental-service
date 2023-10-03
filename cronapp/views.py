import json
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Telemetry
from .tasks import *


def home(request):
    return HttpResponse(f'Hello This is Moovalhalla Django App\n\n')


def telemetry_list(request):
    telemetry_list = Telemetry.objects.all()
    return HttpResponse(render_to_string('telemetry_list.html', {'telemetry_list': telemetry_list}))


def car_list(request):
    car_list = Car.objects.all()
    return HttpResponse(render_to_string('car_list.html', {'car_list': car_list}))


def user_list(request):
    user_list = User.objects.all()
    return HttpResponse(render_to_string('user_list.html', {'user_list': user_list}))


def rental_list(request):
    rental_list = Rental.objects.all()
    return HttpResponse(render_to_string('rental_list.html', {'rental_list': rental_list}))


def create_telemetry(request, number=1):
    create_random_telemetries.delay(number)
    return HttpResponse(f'telemetries generated\n\n')


def create_car(request, number=1):
    create_random_car.delay(number)
    return HttpResponse(f'cars generated')


def create_user(request, number=1):
    create_random_user.delay(number)
    return HttpResponse(f'users generated')


def create_rental(request, number=1):
    create_random_rental.delay(number)

    return HttpResponse(f'rentals generated')
