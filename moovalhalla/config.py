import os
from environs import Env


env = Env()
# Read .env into os.environ
path = os.getcwd()
env.read_env(".env")

SPEED_LIMIT_CHECK_THRESHOLD = env.int('SPEED_LIMIT_CHECK_THRESHOLD', 50)
MAX_SPEED = env.int('MAX_SPEED_LIMIT', 130)
SPEED_LIMIT_CHECK_TIMEOUT = env.int(
    'SPEED_LIMIT_CHECK_TIMEOUT', 10)  # seconds

REDIS_SERVER = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None
REDIS_CONNECT_TIMEOUT = 5
REDIS_SOCKET_TIMEOUT = 5

CACHE_BACKEND = "redis"
