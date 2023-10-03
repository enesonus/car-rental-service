import json

from fastmain import fast_app
import requests
from cronapp.models import Car, User, Rental, Telemetry
from schemas import FastCarCreate, FastUserCreate, FastRentalCreate, FastTelemetryCreate
from utils import process_telemetry


@fast_app.post("/save_telemetry/")
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
        return {"message": "Telemetry created successfully", "telemetry": json.dumps(new_telemetry)}
    except Exception as e:
        return {"error": str(e)}


@fast_app.post("/save_car/")
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


@fast_app.post("/save_user/")
def save_user(user: FastUserCreate):
    try:
        new_user = User.objects.create(first_name=user.first_name, last_name=user.last_name,
                                       email=user.email, phone_number=user.phone_number, date_of_birth=user.date_of_birth)
        return {"message": "User created successfully", "user": new_user}
    except Exception as e:
        return {"error": e}


@fast_app.post("/save_rental/")
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
