from fastmain import fast_app
from cronapp.models import *
from schemas import *


@fast_app.get("/fastapi")
def hello():
    return {"Hello": "World This is FastAPI in Movallhalla"}


@fast_app.get("/get_cars/", response_model=list[FastCar])
def get_cars():
    # Get all cars from the database
    dbcars = Car.objects.all()
    fastcars: FastCar = []
    for car in dbcars:
        fastcars.append(
            FastCar(id=car.id, model=car.model, year=car.year, mileage=car.mileage,
                    fuel_type=car.fuel_type, transmission=car.transmission, color=car.color))
    return fastcars


@fast_app.get("/get_users/", response_model=list[FastUser])
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


@fast_app.get("/get_rentals/", response_model=list[FastRental])
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


@fast_app.get("/get_telemetries/", response_model=list[FastTelemetry])
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
