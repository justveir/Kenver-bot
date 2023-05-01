from config_data.config import WEATHER_API_KEY
from aiogram import Bot, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.enums.dice_emoji import DiceEmoji
import requests

router: Router = Router()


class weather(StatesGroup):
    City = State()

@router.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nЯ многофункциональный бот\nНапиши комманду /commands, чтобы узнать, что я умею.')


@router.message(Command(commands=["commands"]))
async def process_start_command(message: Message):
    await message.answer('/weather - узнай погоду в своем городе\n/dice - игральный кубик')

@router.message(Command(commands=["weather"]))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer("Введите название города")
    await state.set_state(weather.City)

@router.message(StateFilter(weather.City))
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


    await state.clear()

@router.message(Command(commands=["dice"]))
async def cmd_dice(message: types.Message, bot: Bot):
    await message.answer_dice(emoji=DiceEmoji.DICE)



@router.message()
async def info(message: Message):
    await message.reply('Похоже что это неизвестная команда!\nСписок команд вы можете посмотреть с помощью команды /commands')