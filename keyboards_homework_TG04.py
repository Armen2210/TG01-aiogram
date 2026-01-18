from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Привет", callback_data="hello"),
         InlineKeyboardButton(text="Пока", callback_data="bye"),]
    ])

links_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url="https://dzen.ru/news")],
        [InlineKeyboardButton(text="Музыка", url="https://music.yandex.ru/?ysclid=mkk2ehgoqp429343521")],
        [InlineKeyboardButton(text="Видео", url="https://dzen.ru/shorts")]
    ])

dynamic_start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
    ])

dynamic_options_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="opt_1"),
         InlineKeyboardButton(text="Опция 2", callback_data="opt_2")]
    ])