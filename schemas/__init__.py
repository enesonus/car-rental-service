from enum import Enum
from pydantic import BaseModel
from decimal import Decimal
from typing import List, Optional


class TransmissionType(str, Enum):
    AUTOMATIC = 'Automatic'
    MANUAL = 'Manual'


class FuelType(str, Enum):
    GASOLINE = 'Gasoline'
    DIESEL = 'Diesel'
    ELECTRIC = 'Electric'
    HYBRID = 'Hybrid'


class FastCarBase(BaseModel):
    model: Optional[str]
    year: Optional[int]
    mileage: Optional[int]
    fuel_type: Optional[FuelType]
    transmission: Optional[TransmissionType]
    color: Optional[str]


class FastCarCreate(FastCarBase):
    pass


class FastCar(FastCarBase):
    id: int

    class Config:
        orm_mode = True


class FastUserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    date_of_birth: str  # Use appropriate datetime format here


class FastUserCreate(FastUserBase):
    pass


class FastUser(FastUserBase):
    id: int

    class Config:
        orm_mode = True


class FastTelemetryBase(BaseModel):
    car_id: int
    timestamp: str  # Use appropriate datetime format here
    speed: Decimal
    fuel_level: Decimal
    engine_temp: Decimal
    lat: Decimal
    lon: Decimal


class FastTelemetryCreate(FastTelemetryBase):
    pass


class FastTelemetry(FastTelemetryBase):
    id: int

    class Config:
        orm_mode = True


class FastRentalBase(BaseModel):
    car_id: int
    user_id: int
    start_date: str  # Use appropriate datetime format here
    end_date: str  # Use appropriate datetime format here
    total_cost: Decimal


class FastRentalCreate(FastRentalBase):
    pass


class FastRental(FastRentalBase):
    id: int

    class Config:
        orm_mode = True
