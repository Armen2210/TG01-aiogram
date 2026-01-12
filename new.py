import asyncio
import os
import sqlite3

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, FSInputFile
import aiohttp

from dotenv import load_dotenv

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

conn = sqlite3.connect('bot.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    cgat_id INTEGER)''')

conn.commit() # сохраняем изменения
conn.close() # закрываем подключение


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())