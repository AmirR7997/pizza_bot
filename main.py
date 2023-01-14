from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import sqlite3from constant import get_products_query
TOKEN = '5901370716:AAHAdCqATJZ6WSQRUm4buzP-fivEBdkYLuU'

bot = TeleBot(TOKEN, parse_mode = None)

def main_menu_keyboard():
    """
    Эта функция создает первоначальное меню в нашем тг боте

    :return Обьект класса ReplyKeyboardMarkup
    """

    cart = KeyboardButton("Корзина")
    menu = KeyboardButton("Меню")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(menu)
    keyboard.add(cart)

    return keyboard


def get_product_names() -> list:
    products = []

    try:
        conn = sqlite3.connect("Pizza_db")
    except Exception as e:
        print(e)


def menu_keyboard():
    """
    это меню высвечивает товары в нашей базе данных

    :return Обьект класса ReplyKeyboardMarkup
    """

    products = get_product_names()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for product in products:
        button = KeyboardButton(product)
        row.append(button)
        if len(row) == 2:
            keyboard.add(*row)
            row = []


    if row:
        keyboard.add(row[0])
    back_button = KeyboardButton("<< Назад")
    keyboard.add(back_button)

    return keyboard

@bot.message_handler(commands=["start"])
def start_handler(message):
    reply = "Welcome to the hell babe "
    bot.reply_to(message, reply, reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda message: message.text == "Меню")
def menu_handler(message):
    reply = "Выберите свой круг ада"
    bot.reply_to(message,reply,reply_markup = menu_keyboard())







    bot.infinity_polling()
