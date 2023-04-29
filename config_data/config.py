from environs import Env

env = Env()

token = env.str("token")

WEATHER_API_KEY = env.str("WEATHER_API_KEY")