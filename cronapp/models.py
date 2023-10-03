import json
from django.db import models

from enum import Enum


class TransmissionType(Enum):
    AUTOMATIC = 'Automatic'
    MANUAL = 'Manual'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def value_choices(cls):
        return list(i.value for i in cls)


class FuelType(Enum):
    GASOLINE = 'Gasoline'
    DIESEL = 'Diesel'
    ELECTRIC = 'Electric'
    HYBRID = 'Hybrid'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def value_choices(cls):
        return list(i.value for i in cls)


class Car(models.Model):

    model = models.CharField(max_length=100, null=True)
    year = models.PositiveIntegerField(null=True)
    mileage = models.PositiveIntegerField(null=True)
    fuel_type = models.CharField(
        max_length=9, choices=FuelType.choices(), default='1')
    transmission = models.CharField(
        max_length=9, choices=TransmissionType.choices(), default='1')
    color = models.CharField(max_length=20, null=True)


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=80)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateTimeField(auto_now_add=True)


class Telemetry(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    speed = models.DecimalField(max_digits=6, decimal_places=2)
    fuel_level = models.DecimalField(max_digits=5, decimal_places=2)
    engine_temp = models.DecimalField(max_digits=5, decimal_places=2)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)


class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
