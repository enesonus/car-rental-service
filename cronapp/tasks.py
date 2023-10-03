from datetime import date, datetime, timedelta
from celery import shared_task

from schemas import *
from .models import *
import random
import string
import requests


def generate_fake_email():
    username = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=random.randint(5, 10)))
    domain = random.choice(
        ["example.com", "testmail.com", "fakedomain.com", "yourdomain.com"])
    return f"{username}@{domain}"


def generate_date_of_birth():
    eighteenyears = datetime.now() - timedelta(days=365 * 18)  # 18 years ago from today

    return eighteenyears - timedelta(days=random.randint(0, 365 * 52))


def generate_fake_phone_number():
    phone_number = "+90"
    for _ in range(10):
        phone_number += str(random.randint(0, 9))
    return phone_number


turkish_names = [
    "Ahmet", "Ayşe", "Mehmet", "Fatma", "Mustafa", "Emine", "Ali", "Zeynep",
    "Hüseyin", "Hatice", "İbrahim", "Sultan", "Hasan", "Elif", "Hülya", "Murat",
    "Aysel", "Okan", "Nur", "Yusuf", "Sema", "Erdem", "Sevgi", "Emir", "Derya",
    "İsmail", "Yasemin", "Volkan", "Meltem", "Mert", "Aysun", "Orhan", "Ebru",
    "Kadir", "Sedef", "Bilal", "Esra", "Burak", "Ezgi", "Can", "Yeliz", "Deniz",
    "Tuğba", "Ferhat", "Gizem", "Gökhan", "Gül", "Hakan", "İclal", "Hamza"
    # Add more names as needed
]
turkish_lastnames = [
    "Yılmaz", "Kaya", "Demir", "Çelik", "Yıldırım", "Şahin", "Arslan", "Erdoğan",
    "Koç", "Öztürk", "Kara", "Aksoy", "Aslan", "Karadağ", "Taş", "Yalçın", "Aydın",
    "Güneş", "Kurt", "Yıldız", "Eren", "Kaplan", "Turan", "Özdemir", "Kılıç", "Kocaman",
    "Sarı", "Özkan", "Bulut", "Acar", "Ay", "Güler", "Yılmazer", "Çetin", "Özgür",
    "Keskin", "Şimşek", "Eren", "Duman", "Güven", "Toprak", "Taşcı", "Gündoğdu",
    "Kılıç", "Çakır", "Güzel", "Tunç", "Akbulut", "Aydın", "Güzel", "Keskin"
    # Add more last names as needed
]
car_models = [
    "Toyota Corolla", "Honda Civic", "Nissan Altima", "Ford Mustang", "Chevrolet Camaro",
    "BMW 3 Series", "Mercedes-Benz C-Class", "Audi A4", "Hyundai Elantra", "Kia Optima",
    "Volkswagen Golf", "Subaru Outback", "Mazda CX-5", "Lexus RX", "Jeep Wrangler",
    "Tesla Model 3", "Porsche 911", "Ferrari 488", "Lamborghini Huracan", "Aston Martin DB11",
    "Bugatti Chiron", "Land Rover Range Rover", "Volvo XC60", "Jaguar F-Pace", "Dodge Challenger",
    "Chrysler 300", "Lincoln Navigator", "GMC Sierra", "Ram 1500", "Toyota RAV4", "Honda CR-V",
    "Nissan Rogue", "Ford Escape", "Chevrolet Equinox", "BMW X5", "Mercedes-Benz GLE",
    "Audi Q5", "Hyundai Tucson", "Kia Sportage", "Volkswagen Tiguan", "Subaru Forester",
    "Mazda CX-9", "Lexus NX", "Jeep Grand Cherokee", "Tesla Model Y", "Porsche Cayenne",
    "Ferrari F8 Tributo", "Lamborghini Aventador", "Aston Martin Vantage", "Bugatti Veyron"
    # Add more car models as needed
]
colors = [
    "Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Pink", "Brown", "Gray", "Black",
    "White", "Cyan", "Magenta", "Teal", "Lime", "Maroon", "Olive", "Navy", "Silver", "Gold",
    "Indigo", "Turquoise", "Salmon", "Violet", "Coral", "Khaki", "Slate", "Plum", "Azure", "Beige",
    "Crimson", "Fuchsia", "Lavender", "Mint", "Orchid", "Peach", "Raspberry", "Tomato", "Wheat", "Linen",
    "Moccasin", "Periwinkle", "Thistle", "Cornflower", "Chartreuse", "Honeydew", "Ivory", "Misty Rose", "Sandy Brown",
    "Seashell", "Tan"
    # Add more colors as needed
]


@shared_task
def create_random_telemetries(quantity: int):
    new_telemetries = []
    for i in range(quantity):
        try:
            car_id_list = Car.objects.values_list('id', flat=True)
            car_id = random.choice(car_id_list)

            timestamp = datetime.now()
            speed = random.randint(0, 80)
            fuel_level = random.randint(0, 100)
            engine_temp = random.randint(50, 100)
            lat = random.uniform(41.021347, 41.035695)
            lon = random.uniform(29.114176, 29.123484)

            telemetry_json = FastTelemetryCreate(car_id=car_id, timestamp=timestamp.isoformat(), speed=speed,
                                                 fuel_level=fuel_level, engine_temp=engine_temp, lat=lat, lon=lon).json()
            requests.post('http://localhost:8000/save_telemetry',
                          data=telemetry_json)
            new_telemetries.append(telemetry_json)
        except Exception as e:
            return {'error': str(e)}

    return new_telemetries


@shared_task
def create_random_car(quantity: int):

    new_cars = []

    fuel_types = FuelType.value_choices()
    transmission_types = TransmissionType.value_choices()

    for i in range(quantity):
        car = Car.objects.create(
            model=random.choice(car_models),
            year=random.randint(1990, 2021),
            mileage=random.randint(0, 1000000),
            fuel_type=random.choice(fuel_types),
            transmission=random.choice(transmission_types),
            color=random.choice(colors),
        )
        # new_cars.append(car)

    return True


@shared_task
def create_random_user(quantity: int):
    new_users = []

    for i in range(quantity):

        user = User.objects.create(
            first_name=random.choice(turkish_names),
            last_name=random.choice(turkish_lastnames),
            email=generate_fake_email(),
            phone_number=generate_fake_phone_number(),
            date_of_birth=generate_date_of_birth(),
        )

        # new_users.append(user)

    return True


@shared_task
def create_random_rental(quantity: int):

    new_rentals = []
    for i in range(quantity):
        car_id_list = Car.objects.values_list('id', flat=True)
        user_id_list = User.objects.values_list('id', flat=True)
        car_id = random.choice(car_id_list)
        user_id = random.choice(user_id_list)

        start_date = datetime.now() + timedelta(days=random.randint(0, 30))
        end_date = start_date + \
            timedelta(hours=random.randint(0, 1),
                      minutes=random.randint(0, 59))
        delta = end_date - start_date

        rental = Rental.objects.create(
            car=Car.objects.get(id=car_id),
            user=User.objects.get(id=user_id),
            start_date=start_date,
            end_date=end_date,
            total_cost=(delta.total_seconds()/60) * 7,
        )
        # new_rentals.append(rental)

    return True
