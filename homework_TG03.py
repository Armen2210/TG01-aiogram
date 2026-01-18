import asyncio
import os
import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
import logging

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


if not BOT_TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в .env (добавь строку BOT_TOKEN=...)")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
  name = State()
  age = State()
  grade = State()

def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade TEXT NOT NULL)
    ''')

    conn.commit() # сохраняем изменения
    conn.close() # закрываем подключение

init_db()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer('Привет, я бот помощник! Напиши свое имя') # вызываем функцию "start", после нам задают вопрос: имя?
    await state.set_state(Form.name) # программа ожидает имя, чтобы сохранить

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text) # ответ обрабатывается и сохраняется
    await message.answer('Сколько тебе лет?') # задаем следующий вопрос
    await state.set_state(Form.age) # программа ожидает возраст, чтобы сохранить

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text) # ответ обрабатывается и сохраняется
    await message.answer('Из какого ты класса?') # задаем следующий вопрос
    await state.set_state(Form.grade) # программа ожидает город, чтобы сохранить

@dp.message(Form.grade)
async def grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text) # ответ обрабатывается и сохраняется
    user_data = await state.get_data() # извлекает все данные, которые были получены и делает словарь

    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO students(name, age, grade) VALUES (?, ?, ?)''', (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()  # сохраняем изменения
    conn.close()  # закрываем подключение

    student_info = (f"Имя - {user_data['name']}\n"
                    f"Возраст - {user_data['age']}\n"
                    f"Класс - {user_data['grade']}\n")
    await message.answer(student_info)

    await state.clear()



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())