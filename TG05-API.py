import asyncio
import os
from http.client import responses

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from datetime import datetime, timedelta
import random
import requests


from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
THE_CAT_API_KEY = os.getenv('THE_CAT_API_KEY')
NASA_API_KEY = os.getenv('NASA_API_KEY')

if not BOT_TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в .env (добавь строку BOT_TOKEN=...)")

if not THE_CAT_API_KEY:
    raise RuntimeError("Не найден THE_CAT_API_KEY в .env (добавь строку THE_CAT_API_KEY=...)")

if not NASA_API_KEY:
    raise RuntimeError("Не найден NASA_API_KEY в .env (добавь строку NASA_API_KEY=...)")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Вот в этом промежутке мы будем работать и писать новый код
def get_cat_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def get_cat_image_by_breed(breed_id):
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data [0]['url']

def get_breed_info(breed_name):
    breeds = get_cat_breeds()
    for breed in breeds:
        if breed ['name'].lower() == breed_name.lower():
            return breed
    return None # вернет, если такой породы не было

def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date +(end_date - start_date) * random.random()
# random.random() выдает число от 0 до 1, всегда нецелое число
# end_date - start_date - конечная дата минус стартовая дата - это 365 дней
    date_str = random_date.strftime("%Y-%m-%d")

    url = (f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}')
    response = requests.get(url)
    return response.json()

def get_yesno():
    url = "https://yesno.wtf/api"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()


@dp.message(CommandStart())
async def start(message:Message):
    await message.answer(f'Привет {message.from_user.first_name}!'
                         f' Напиши мне название породы кошки, и я пришлю тебе её фото и описание.')


@dp.message(Command('random_apod'))
async def random_apod(message: Message):
    apod = get_random_apod()
    photo_url = apod.get('url')
    title = apod.get('title', 'NASA APOD')

    await message.answer_photo(photo=photo_url, caption=title)


@dp.message(Command("yesno_cmd"))
async def yesno_cmd(message:Message):
    data = get_yesno()
    await message.answer_animation(animation=data["image"], caption=f"Ответ: {data['answer']}")


@dp.message()
async def send_cat_info(message:Message):
    breed_name = message.text
    breed_info = get_breed_info(breed_name)
    if breed_info:
        cat_image_url = get_cat_image_by_breed(breed_info['id'])
        info = (f'Порода - {breed_info["name"]}\n'
                f'Описание - {breed_info["description"]}\n'
                f'Продолжительность жизни - {breed_info["life_span"]} лет')
        await message.answer_photo(photo=cat_image_url, caption=info)
    else:
        await message.answer('Порода не найдена')







async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())