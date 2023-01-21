from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import sqlite3
from constant import get_products_query, create_new_user_query
from utils import MenuStack
TOKEN = '5901370716:AAHAdCqATJZ6WSQRUm4buzP-fivEBdkYLuU'

bot = TeleBot(TOKEN, parse_mode = None)


def main_menu_keyboard():
    """
    Эта функция создает первоначальное меню в нашем тг боте
    :return Обьект класса ReplyKeyboardMarkup
    """

    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    cart = KeyboardButton("Корзина🧺")
    menu = KeyboardButton("Меню🍔")
    settings = KeyboardButton("Настройки⚙️")
    delivery = KeyboardButton("Доставка🚚")
    rep = KeyboardButton("Отзывы и предложения📝")
    contacts = KeyboardButton("Контакты☎️")

    markup.add(cart)
    markup.add(menu, contacts)
    markup.add(settings, delivery, rep)

    return markup

stack = MenuStack(main_menu_keyboard())


def get_product_names() -> list:
    products = []

    try:
        conn = sqlite3.connect("Pizza_db")
        cursor = conn.cursor()
        sql = get_products_query()
        cursor.execute(sql)

        for product in cursor.fetchall():
            products.append(product[0])

    except Exception as e:
        print(e)

    return products

def menu_keyboard():
    '''это меню высвечивает товары в нашей базе данных
    :return Обьект класса ReplyKeyboardMarkup'''

    products = get_product_names()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for product in products:
        button = KeyboardButton(product)
        row.append(button)
        if len(row) == 3:
            keyboard.add(*row)
            row = []


    if row:
        keyboard.add(row[0])
    back_button = KeyboardButton("Назад🔙")
    keyboard.add(back_button)

    return keyboard

def get_user_details_keyboard(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    phone_exist = False
    address_exist = False
    if not check_phone_number(chat_id):
        get_phone_button = KeyboardButton("Введите номер телефона ")
        markup.add(get_phone_button)
    else:
        phone_exist = True

    if not check_address(chat_id):
        get_address_button = KeyboardButton("Введите ваш адресс")
        markup.add(get_address_button)
    else:
        address_exist = True
    if phone_exist and address_exist:
        keyboard = main_menu_keyboard()


    return  markup

def create_user(chat_id):
    try:
        conn = sqlite3.connect('Pizza_db')
        cursor = conn.cursor()
        sql = create_new_user_query(chat_id)
        cursor.execute(sql)

    except Exception as e:
        print(e)



@bot.message_handler(commands=["start"])
def start_handler(message):
    chat_id = message.chat.id

    create_user(chat_id)

    reply = f"Welcome to the hell {message.from_user.first_name} "
    bot.reply_to(message, reply, reply_markup=get_user_details_keyboard())
    print(f'Name_of_user - {message.from_user.first_name}')
    print(f'Username_of_user - @{message.from_user.username}')
    print(f'ID_user - {message.from_user.id}')

@bot.message_handler(func=lambda message: message.text == "Меню🍔")
def menu_handler(message):
    reply = "Выберите пиццу"
    bot.reply_to(message, reply, reply_markup=menu_keyboard())
    stack.push(menu_keyboard())

@bot.message_handler(content_types=['text'])
def message_handler(message):

    if message.text == "Меню🍔":
        bot.reply_to(message, 'Выбери пиццу:🍕', reply_markup=menu_keyboard())
    if message.text == "Настройки⚙️":
        bot.reply_to(message, '-Пока что это:💩-', reply_markup=back_keyboard())
    if message.text == "Корзина🧺":
        bot.reply_to(message, '-Пока что это:💩-', reply_markup=back_keyboard())
    if message.text == "Доставка🚚":
        bot.reply_to(message,
                     'Если мы не успеем доставить заказ в течении 60 минут, то мы отправим вам промокод на бесплатную пиццу🎁\n\n'
                     '- Доставка бесплатная✅\n'
                     '- Доставим при заказе от 50.000 sum💴\n'
                     'P.S скопированно с тг бота додо пиццы')
    if message.text == "Отзывы и предложения📝":
        bot.reply_to(message, ':Дорогой клиент\n'
                              'Спасибо, что выбираете нас\n'
                              'Оцените работу нашей команды от 1 до 5', reply_markup=feedback_keyboard())

    if message.text == 'Назад🔙':
        bot.reply_to(message, f'Добро пожаловать<b>{message.from_user.first_name}💛</b>!\n'
                                f'Что желаете заказать?', parse_mode='html', reply_markup=main_menu_keyboard())

    if message.text == '😊 Мне все понравилось, 5 ❤️':
        bot.reply_to(message, 'Мы рады, что вы выбираете нас, надеемся на наше дальнейшее сотрудничество🤗\n ВашDodoPizza ❤️',
                    reply_markup=main_menu_keyboard())

    if message.text == '☺️Нормально, 4 ⭐️⭐️⭐️⭐️':
        bot.reply_to(message, 'Мы рады, что вам понравилось 😊. Что мы можем сделать, чтобы улучшить наш сервис?🤔',
                    reply_markup=back_keyboard())

    if message.text == 'Назад⬅️':
        bot.reply_to(message, 'Что желаете заказать?🍔', reply_markup=main_menu_keyboard())
    if message.text == '😐 Удовлетворительно, 3 ⭐️⭐️⭐️':
        bot.reply_to(message, 'Мы сожалеем, что нам не удалось оправдать ваших ожиданий.\n'
                              'Помогите нам стать лучше, оставьте свой комментарий или предложение для улучшения качества обслуживания  👇🏻.\n'
                              'Мы будем работать над вашими предложениями, чтобы стать лучше  🙏🏻', reply_markup=back_keyboard())

    if message.text == "☹️Мне не зашло, 2 ⭐️⭐️":
        bot.reply_to(message, 'Мы сожалеем, что разочаровали вас.\n'
                              'Помогите нам стать лучше, оставьте свой комментарий или предложение для улучшения качества обслуживания 👇🏻.\n'
                              'Мы будем работать над вашими предложениями, чтобы стать лучше 🙏🏻', reply_markup=back_keyboard())
    if message.text == 'Контакты☎️':
        bot.reply_to(message, '- Номер телефона: +998(97)157-79-97\n- Звонок бесплатный✅', reply_markup=main_menu_keyboard())

'''def menu_pizza_keyboard():
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    button1 = KeyboardButton('Пеперони🍕')
    button2 = KeyboardButton('Маргарита🍕')
    button3 = KeyboardButton('Гавайская🍕')
    button4 = KeyboardButton('Комбо🍕')
    button5 = KeyboardButton('4 сыра🍕')
    button6 = KeyboardButton('Цыпленок ранч🍕')
    button7 = KeyboardButton('🔙')

    markup.add(button1,button2,button3)
    markup.add(button4,button5,button6)
    markup.add(button7)


    return markup'''

def feedback_keyboard():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    button1 = KeyboardButton('😊 Мне все понравилось, 5 ❤️')
    button2 = KeyboardButton('☺️Нормально, 4 ⭐️⭐️⭐️⭐️')
    button3 = KeyboardButton('😐 Удовлетворительно, 3 ⭐️⭐️⭐️')
    button4 = KeyboardButton('☹️Мне не зашло, 2 ⭐️⭐️')

    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    markup.add(button4)


    return markup



def back_keyboard():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    button = KeyboardButton('Назад⬅️')
    markup.add(button)

    return markup

@bot.message_handler(func=lambda message: message.text == "Назад⬅️")
def back_handler(message):
    menu_to_go_back = stack.pop()
    bot.send_message(message.chat.id, "Прошлое меню: ", reply_markup=menu_to_go_back)

bot.infinity_polling()























