import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from dotenv import load_dotenv

import keyboards_homework_TG04 as kb

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Приветствую, {message.from_user.full_name}! Я твой бот помощник!",
        reply_markup=kb.inline_keyboard_test
    )


@dp.callback_query(F.data == "hello")
async def hello(callback: CallbackQuery):
    name = callback.from_user.full_name
    await callback.answer()
    await callback.message.answer(f"Привет, {name}!")


@dp.callback_query(F.data == "bye")
async def bye(callback: CallbackQuery):
    name = callback.from_user.full_name
    await callback.answer()
    await callback.message.answer(f"До свидания, {name}!")


@dp.message(Command("links"))
async def links(message: Message):
    await message.answer("Выбери, куда перейти:", reply_markup=kb.links_keyboard)


@dp.message(Command("dynamic"))
async def dynamic(message: Message):
    await message.answer(
        "Нажми кнопку ниже:",
        reply_markup=kb.dynamic_start_keyboard
    )


@dp.callback_query(F.data == "show_more")
async def show_more(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Выбери опцию:",
        reply_markup=kb.dynamic_options_keyboard
    )


@dp.callback_query(F.data == "opt_1")
async def opt_1(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Опция 1")


@dp.callback_query(F.data == "opt_2")
async def opt_2(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Опция 2")




async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
