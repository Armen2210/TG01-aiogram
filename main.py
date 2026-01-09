import asyncio
import os
import random
import requests

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY", "Moscow")

if not BOT_TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в .env (добавь строку BOT_TOKEN=...)")

if not OPENWEATHER_API_KEY:
    raise RuntimeError("Не найден OPENWEATHER_API_KEY в .env (добавь строку OPENWEATHER_API_KEY=...)")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def get_weather_text(city: str) -> str:
    """
    Получаем погоду из OpenWeatherMap и возвращаем готовый текст.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",   # чтобы градусы были в °C
        "lang": "ru"         # описание погоды на русском
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

        return (
            f"Погода в городе {city}:\n"
            f"🌤 {description}\n"
            f"🌡 Температура: {temp}°C (ощущается как {feels_like}°C)\n"
            f"💨 Ветер: {wind} м/с"
        )

    except requests.exceptions.RequestException:
        return "Не получилось получить погоду 😕 Проверь интернет или попробуй позже."
    except (KeyError, TypeError, ValueError):
        return "Получил странный ответ от сервиса погоды 😕 Попробуй позже."


@dp.message(Command("weather"))
async def weather(message: Message):
    # ВАЖНО: requests блокирует поток, но для учебного проекта и простоты это ок.
    text = get_weather_text(CITY)
    await message.answer(text)


@dp.message(Command('photo'))
async def photo(message=Message):
    list = ['https://img.freepik.com/free-photo/cartoon-style-hugging-day-celebration_23-2151033271.jpg', 'https://img.goodfon.ru/wallpaper/nbig/c/c9/enot-vzgliad-voda-pogruzhenie-morda.webp', 'https://news.artnet.com/app/news-upload/2015/09/c6e48da82c0e49d1a012971e652a5132-1560x2158-1480x2048.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Лови прикольную картинку')


@dp.message(F.photo)
async def react_photo(message=Message):
    list = ['Ух ты!', 'Ничего себе!', 'Веселые картинки)']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)


@dp.message(F.text == 'Что такое ИИ?')
async def aitext(message=Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(Command('help'))
async def help(message=Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /photo \n /help')

@dp.message(CommandStart())
async def start(message=Message):
    await message.answer('Приветствую! Я твой бот помощник!')



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
