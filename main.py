import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv
import random


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в .env (добавь строку BOT_TOKEN=...)")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('photo'))
async def photo(message=Message):
    list = ['https://img.freepik.com/free-photo/cartoon-style-hugging-day-celebration_23-2151033271.jpg', 'https://img.goodfon.ru/wallpaper/nbig/c/c9/enot-vzgliad-voda-pogruzhenie-morda.webp', 'https://news.artnet.com/app/news-upload/2015/09/c6e48da82c0e49d1a012971e652a5132-1560x2158-1480x2048.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Лови ссылку на картинку')


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
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help')

@dp.message(CommandStart())
async def start(message=Message):
    await message.answer('Приветствую! Я твой бот помощник!')



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
