import string
import requests
from schemas import FastCarCreate, FastUserCreate, FastRentalCreate, FastTelemetryCreate
from django.core.cache import cache
from moovalhalla import config


def get_speed_limit_at(lat: float, lon: float):
    url = "https://valhalla.dev.moovtr.com/trace_attributes"
    session = requests.Session()
    payload = {
        "shape": [
            {
                "lat": f"{lat}",
                "lon": f"{lon}"
            },
            {
                "lat": f"{lat}",
                "lon": f"{lon}"
            }
        ],
        "costing": "auto",
        "shape_match": "map_snap",
        "filters": {
            "attributes": [
                "edge.speed",
                "edge.names"
            ],
            "action": "include"
        }
    }

    try:
        response = session.post(url, json=payload, timeout=2)

        data = response.json()
        edge_keys = data["edges"][0].items()

        try:
            for key, value in edge_keys:
                if key == 'speed':
                    return value
        except:
            value = None

    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")


def check_speed_limit_at(lat: float, lon: float, speed: float, car_id: string):

    if not cache.get(f"speed_limit_exceeded_{car_id}") and speed > config.SPEED_LIMIT_CHECK_THRESHOLD:
        if speed > config.MAX_SPEED:
            cache.set(
                f"speed_limit_exceeded_{car_id}", True,
                timeout=config.SPEED_LIMIT_CHECK_TIMEOUT)
            print(
                f"Max Speed limit exceeded\nCurrent speed:{speed}\nMax speed limit: {config.MAX_SPEED}\nCar ID:{car_id}\nat {lat}, {lon}\n\n")
        else:
            speed_limit = get_speed_limit_at(lat, lon)
            if speed_limit and speed > speed_limit:
                cache.set(
                    f"speed_limit_exceeded_{car_id}", True, timeout=config.SPEED_LIMIT_CHECK_TIMEOUT)
                print(
                    f"Speed limit exceeded\ncurrent speed:{speed}\nspeed limit: {speed_limit}\nCar ID:{car_id}\nat {lat}, {lon}\n\n")


def process_telemetry(telemetry: FastTelemetryCreate):

    check_speed_limit_at(lat=telemetry.lat, lon=telemetry.lon,
                         speed=telemetry.speed, car_id=telemetry.car_id)
