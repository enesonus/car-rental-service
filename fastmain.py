import os

from moovalhalla.wsgi import application as django_application
from cronapp.models import *
from schemas import *
from apis.utils import process_telemetry

from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

import uvicorn

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moovalhalla.settings")


fast_app = FastAPI()


@fast_app.post("/save_telemetry")
def save_telemetry(telemetry: FastTelemetryCreate):
    try:

        process_telemetry(telemetry)

        new_telemetry = Telemetry.objects.create(
            car_id=telemetry.car_id,
            timestamp=telemetry.timestamp,
            speed=telemetry.speed,
            fuel_level=telemetry.fuel_level,
            engine_temp=telemetry.engine_temp,
            lat=telemetry.lat,
            lon=telemetry.lon,
        )
        return {"message": "Telemetry created successfully", "telemetry": new_telemetry}
    except Exception as e:
        return {"error": str(e)}


@fast_app.post("/save_car")
def save_car(car: FastCarCreate):
    # Save a car
    try:
        new_car = Car.objects.create(
            model=car.model,
            year=car.year,
            mileage=car.mileage,
            fuel_type=car.fuel_type,
            transmission=car.transmission,
            color=car.color,
        )
        return {"message": "Car created successfully", "car": new_car}
    except Exception as e:
        return {"error": e}


@fast_app.post("/save_user")
def save_user(user: FastUserCreate):
    try:
        new_user = User.objects.create(first_name=user.first_name, last_name=user.last_name,
                                       email=user.email, phone_number=user.phone_number, date_of_birth=user.date_of_birth)
        return {"message": "User created successfully", "user": new_user}
    except Exception as e:
        return {"error": e}


@fast_app.post("/save_rental")
def save_rental(rental: FastRentalCreate):
    try:
        new_rental = Rental.objects.create(
            car_id=rental.car_id,
            user_id=rental.user_id,
            start_date=rental.start_date,
            end_date=rental.end_date,
            total_cost=rental.total_cost,
        )
        return {"message": "Rental created successfully", "rental": new_rental}
    except Exception as e:
        return {"error": str(e)}


@fast_app.get("/fastapi")
def hello():
    return {"Hello": "World This is FastAPI in Movallhalla"}


@fast_app.get("/get_cars", response_model=list[FastCar])
def get_cars():
    # Get all cars from the database
    dbcars = Car.objects.all()
    fastcars: FastCar = []
    for car in dbcars:
        fastcars.append(
            FastCar(id=car.id, model=car.model, year=car.year, mileage=car.mileage,
                    fuel_type=car.fuel_type, transmission=car.transmission, color=car.color))
    return fastcars


@fast_app.get("/get_users", response_model=list[FastUser])
def get_users():
    # Get all users from the database
    dbusers = User.objects.all()
    fastusers: FastCar = []
    for user in dbusers:
        fastusers.append(
            FastUser(id=user.id, first_name=user.first_name, last_name=user.last_name,
                     email=user.email, phone_number=user.phone_number, date_of_birth=user.date_of_birth.isoformat())
        )
    return fastusers


@fast_app.get("/get_rentals", response_model=list[FastRental])
def get_rentals():
    db_rentals = Rental.objects.all()
    fast_rentals = []
    for rental in db_rentals:
        fast_rentals.append(
            FastRental(
                id=rental.id,
                car_id=rental.car.id,
                user_id=rental.user.id,
                start_date=rental.start_date.isoformat(),
                end_date=rental.end_date.isoformat(),
                total_cost=rental.total_cost,
            )
        )
    return fast_rentals


# @fast_app.get("/get_telemetries", response_model=list[FastTelemetry])
def get_telemetries():
    db_telemetries = Telemetry.objects.all()
    fast_telemetries = []
    for telemetry in db_telemetries:
        fast_telemetries.append(
            FastTelemetry(
                id=telemetry.id,
                car_id=telemetry.car.id,
                timestamp=telemetry.timestamp.isoformat(),
                speed=telemetry.speed,
                fuel_level=telemetry.fuel_level,
                engine_temp=telemetry.engine_temp,
                lat=telemetry.lat,
                lon=telemetry.lon,
            )
        )
    return fast_telemetries


# This part is Django please insert fastapi codes above these lines
fast_app.mount("/static",
               StaticFiles(
                   directory='static'
               ),
               name="static",
               )
fast_app.mount("/", WSGIMiddleware(django_application))

if __name__ == '__main__':
    uvicorn.run("fastmain:fast_app", port=8000, host='localhost', reload=True)
