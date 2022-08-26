from loader import bot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup



def keyboards_button(user_id: int) -> None:
    """Функция кнопки"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text='Присоединиться', url='https://t.me/StockNews100')
    keyboard.add(button)
    bot.send_message(user_id, text='нажми', reply_markup=keyboard)
