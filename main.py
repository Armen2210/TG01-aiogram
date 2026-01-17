import asyncio
import os
import random
import requests

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from gtts import gTTS
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
import keyboards as kb


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
print("BOT_TOKEN:", repr(BOT_TOKEN))

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
async def photo(message: Message):
    list = ['https://img.freepik.com/free-photo/cartoon-style-hugging-day-celebration_23-2151033271.jpg', 'https://img.goodfon.ru/wallpaper/nbig/c/c9/enot-vzgliad-voda-pogruzhenie-morda.webp', 'https://news.artnet.com/app/news-upload/2015/09/c6e48da82c0e49d1a012971e652a5132-1560x2158-1480x2048.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Лови прикольную картинку')

@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('HEPyKwIAAAA.mp4')
    await bot.send_video(message.chat.id, video)

@dp.message(Command('voice'))
async def voice(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    voice = FSInputFile('audio_2026-01-09_17-40-22.ogg')
    await message.answer_voice(voice)

@dp.message(Command('audio'))
async def audio(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    audio = FSInputFile('Сигнал частотой 432 Герца (Hz).mp3')
    await bot.send_video(message.chat.id, audio)

@dp.message(Command('doc'))
async def doc(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_document')
    doc = FSInputFile('rest_api.pdf')
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1:\\n1. Скручивания: 3 подхода по 15 повторений\\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2:\\n1. Подъемы ног: 3 подхода по 15 повторений\\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3:\\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

    tts = gTTS(text=rand_tr, lang='ru')
    tts.save('training.mp3')
    audio = FSInputFile('training.mp3')
    await bot.send_audio(message.chat.id, audio)
    os.remove('training.mp3')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ух ты!', 'Ничего себе!', 'Веселые картинки)']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')


@dp.message(F.text == 'Что такое ИИ?')
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')

@dp.message(Command("en"))
async def translate_to_en(message: Message):
    # Берем текст после команды /en
    text_to_translate = message.text.replace("/en", "", 1).strip()

    if not text_to_translate:
        await message.answer("Напиши текст после команды. Пример:\n/en Привет, как дела?")
        return

    try:
        translated = GoogleTranslator(source="auto", target="en").translate(text_to_translate)
        await message.answer(f"🇬🇧 Перевод:\n{translated}")
    except Exception:
        await message.answer("Не получилось перевести текст 😕 Попробуй позже.")


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /photo \n /video \n /voice \n /audio \n /doc \n /training \n /weather \n /en \n /help')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Приветствую, {message.from_user.full_name}! Я твой бот помощник!', reply_markup=kb.inline_keyboard_test)

@dp.message(F.text == 'Тестовая кнопка 1')
async def test_button(message: Message):
    await message.answer('Обработка нажатия на reply кнопку')

# @dp.callback_query(F.data == 'news')
# async def news(callback: CallbackQuery):
#     await callback.answer('новости загружаются', show_alert=True)
#     await callback.message.answer('Вот свежие новости')

@dp.callback_query(F.data == 'news')
async def news(callback: CallbackQuery):
    await callback.answer('новости загружаются', show_alert=True)
    await callback.message.edit_text('Вот свежие новости', reply_markup=await kb.test_keyboard())


@dp.message()
async def echo(message: Message):
    await message.send_copy(chat_id=message.chat.id)



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
