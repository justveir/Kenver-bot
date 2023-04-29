from config_data.config import token, WEATHER_API_KEY
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.enums.dice_emoji import DiceEmoji
import requests, logging
from config_data.config import token, WEATHER_API_KEY
from pprint import pprint

API_TOKEN: str = token

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

class weather(StatesGroup):
    City = State()

def logger():
    logging.basicConfig(level=logging.INFO)


    handler = logging.StreamHandler()
    handler.setLevel(logging.ERROR)


    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)


    logger = logging.getLogger('aiogram')
    logger.addHandler(handler)
logger()

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nЯ многофункциональный бот\nНапиши комманду /commands, чтобы узнать, что я умею.')


@dp.message(Command(commands=["commands"]))
async def process_start_command(message: Message):
    await message.answer('/weather - узнай погоду в своем городе\n/dice - игральный кубик')

@dp.message(Command(commands=["weather"]))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer("Введите название города")
    await state.set_state(weather.City)

@dp.message(StateFilter(weather.City))
async def get_weather(message: Message, state: FSMContext):


    try:
        city = message.text
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        )
        data = r.json()

        cur_weather = data["main"]["temp"]



        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        await message.reply(
              f"Погода в городе: {city}\n\nТемпература: {cur_weather}C°\n"
              f"Влажность: {humidity}%\n\nВетер: {wind} м/с\n\n"
              )

    except:
        await message.reply("Неверное название города! Проверьте правильность написания города.")
        logger.exception("Произошла неизвестная ошибка!")
        pprint(data)

    await state.clear()

@dp.message(Command(commands=["dice"]))
async def cmd_dice(message: types.Message, bot: Bot):
    await message.answer_dice(emoji=DiceEmoji.DICE)

if __name__ == '__main__':
    dp.run_polling(bot)
